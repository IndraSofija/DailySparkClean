from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
import os
import logging
import socket
import time
from datetime import datetime

# Ielādē .env mainīgos
load_dotenv()

# Inicializē FastAPI
app = FastAPI()

# ✅ Atļaut CORS tikai no Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dailyspark-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging iestatījumi
logging.basicConfig(level=logging.INFO)

# 🔐 Debug: pārbaudi, vai API_KEY vispār tiek saņemts
api_key = os.getenv("OPENAI_API_KEY")
print("🔐 API key (sākums):", api_key[:10] if api_key else "None")

client = OpenAI()

# ✅ RAM datubāze dzirksteļu ierobežošanai
user_data = {}

@app.get("/")
def root():
    return {"message": "DailySpark backend is running."}

@app.post("/generate")
async def generate_text(request: Request):
    logging.info("🚀 API /generate saņemts!")

    try:
        body = await request.json()
        niche = body.get("niche")
        prompt = f"Generate a {niche.lower()} inspirational sentence."
        user_id = body.get("user_id")

        if not niche:
            return {"error": "Niche is required."}
        if not user_id:
            return {"error": "User ID is missing."}

        today = datetime.utcnow().date().isoformat()

        user_entry = user_data.get(user_id, {
            "last_reset_date": today,
            "sparks_used_today": 0
        })

        if user_entry["last_reset_date"] != today:
            user_entry["last_reset_date"] = today
            user_entry["sparks_used_today"] = 0

        if user_entry["sparks_used_today"] >= 1:
            return {"error": "Spark limit reached. Try again tomorrow."}

        user_entry["sparks_used_today"] += 1
        user_data[user_id] = user_entry

        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result = chat_completion.choices[0].message.content.strip()
        return {"result": result}

    except Exception as e:
        logging.error(f"⚠️ Error during generation: {e}")
        return {"error": str(e)}

    except Exception as e:
        logging.error(f"⚠️ Kļūda ģenerēšanas laikā: {e}")
        return {"error": str(e)}

        if user_entry["sparks_used_today"] >= 1:
            return {"error": "Spark limit reached. Try again tomorrow."}

    
    except Exception as e:
        logging.error(f"⚠️ Kļūda ģenerēšanas laikā: {e}")
        return {"error": str(e)}

# ✅ Tīkla savienojuma pārbaude ar OpenAI API
@app.get("/network-test")
def network_test():
    try:
        host = "api.openai.com"
        port = 443
        ip = socket.gethostbyname(host)
        s = socket.create_connection((ip, port), timeout=5)
        s.close()
        return {"status": "SUCCESS", "ip": ip}
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

@app.get("/reset-daily-sparks")
def reset_daily_sparks():
    logging.info("🔁 Daily sparks reset initiated!")
    return {"status": "RESET_OK"}

# 👉 Reģistrē dzirksteles saglabāšanas maršrutu
from save_spark import router
app.include_router(router)




