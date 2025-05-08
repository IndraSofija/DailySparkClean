from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
import os
import logging
import socket
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

# ✅ RAM "datubāze" lietotāja datiem
user_data = {}

@app.get("/")
def root():
    return {"message": "DailySpark backend is running."}

@app.post("/generate")
async def generate_text(request: Request):
    logging.info("🚀 API /generate saņemts!")

    try:
        body = await request.json()
        prompt = body.get("prompt")
        user_id = body.get("user_id")

        if not prompt:
            return {"error": "Prompt is required."}

        if not user_id:
            return {"error": "User ID is missing."}

        today = datetime.utcnow().date().isoformat()

        user_entry = user_data.get(user_id, {
            "sparks_used_today": 0,
            "last_reset_date": today
        })

        # Ja ir jauna diena, atiestata skaitītāju
        if user_entry["last_reset_date"] != today:
            user_entry["sparks_used_today"] = 0
            user_entry["last_reset_date"] = today

        if user_entry["sparks_used_today"] >= 1:
            return {"error": "Daily limit reached. Come back tomorrow!"}

        # ✅ Pieaudzina skaitītāju
        user_entry["sparks_used_today"] += 1
        user_data[user_id] = user_entry

