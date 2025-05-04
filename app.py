from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
import os
import logging

import requests

try:
    response = requests.get("https://api.openai.com/v1/models", timeout=5)
    print("✅ Railway var sasniegt OpenAI API. Statusa kods:", response.status_code)
except requests.exceptions.RequestException as e:
    print("❌ Railway NEVAR sasniegt OpenAI API:", e)

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

        # ✅ JAUNĀS API SINTAKSES IZMANTOJUMS
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
