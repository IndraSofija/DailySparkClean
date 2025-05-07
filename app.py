from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
import os
import logging
import socket
import time

# Ielādē .env mainīgos
load_dotenv()

# Inicializē FastAPI
app = FastAPI()

# Atļaut visus CORS pieprasījumus (frontenda testēšanai)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

# Lietotāja pēdējās dzirksteles ģenerēšanas laiks (vienkāršai versijai)
last_generation_time = {}

@app.get("/")
def root():
    return {"message": "DailySpark backend is running."}

@app.post("/generate")
async def generate_text(request: Request):
    logging.info("🚀 API /generate saņemts!")

    try:
        body = await request.json()
        prompt = body.get("prompt")

        if not prompt:
            return {"error": "Prompt is required."}

        user_id = "default_user"  # Vietturis, vēlāk jāaizstāj ar īstu lietotāju ID
        current_time = int(time.time())
        cooldown_seconds = 86400  # 24 stundas

        if user_id in last_generation_time:
            elapsed = current_time - last_generation_time[user_id]
            if elapsed < cooldown_seconds:
                seconds_remaining = cooldown_seconds - elapsed
                return {"error": f"Spark limit reached. Try again in {seconds_remaining} seconds."}

        last_generation_time[user_id] = current_time

        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result = chat_completion.choices[0].message.content.strip()
        return {"result": result}

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
    # Šeit būtu reāla dzirksteļu atjaunošanas loģika, piemēram:
    return {"status": "RESET_OK"}
