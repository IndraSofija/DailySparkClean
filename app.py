from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
import os
import logging
import socket
import time
import random
from datetime import datetime
from get_saved_sparks import router as get_saved_sparks_router
from user_info import user_info
from stripe_webhook import router as stripe_webhook_router
from fix_timestamps import router as fix_timestamps_router
app.include_router(fix_timestamps_router)

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

# 🎯 Nišu randomizācija
niches = [
    "Time to shine",
    "Idea Generator",
    "I know better",
    "Your camera, your story",
    "My opinion matters"
]

def get_random_niche():
    return random.choice(niches)

@app.get("/")
def root():
    return {"message": "DailySpark backend is running."}

@app.post("/generate")
async def generate_text(request: Request):
    logging.info("🚀 API /generate saņemts!")

    try:
        body = await request.json()
        user_id = body.get("user_id")
        subscription_level = body.get("subscription_level")  # <- Jānodrošina no frontend

        if subscription_level == "free":
            niche = get_random_niche()
        else:
            niche = body.get("niche")

        if not niche:
            return {"error": "Niche is required."}
        if not user_id:
            return {"error": "User ID is missing."}

        prompt = f"Generate a {niche.lower()} inspirational sentence."
        print(f"🐾 Saņemtais user_id no pieprasījuma: {user_id}")
        print(f"🌟 Izmantotā niša: {niche}")

        # TESTS: pārbaudām, vai Mongo atrod šo user_id ar regex
        from db import get_user_collection
        users_collection = get_user_collection()
        test_user = await users_collection.find_one({ "user_id": { "$regex": f"^{user_id}$", "$options": "i" } })
        print(f"🔍 Testa vaicājums atrada: {test_user}")

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

        return {
            "result": result,
            "niche": niche
        }

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

@app.get("/user-info")
async def get_user_info(request: Request):
    return await user_info(request)

# 👉 Reģistrē dzirksteles saglabāšanas maršrutu
from save_spark import router
app.include_router(router)

from checkout import router as checkout_router
app.include_router(checkout_router)

from stripe_webhook import router as stripe_router
app.include_router(stripe_router)
app.include_router(get_saved_sparks_router)
app.include_router(stripe_webhook_router)
