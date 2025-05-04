from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import openai
import os
import logging

# Ielādē .env mainīgos
load_dotenv()

# 🔐 Debug: pārbaudi, vai API_KEY vispār tiek saņemts
api_key = os.getenv("OPENAI_API_KEY")
print("🔐 API key (sākums):", api_key[:10] if api_key else "None")

# Inicializē OpenAI klientu — drošā metode (nevis OpenAI(...))
openai.api_key = api_key

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

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content.strip()
        return {"result": result}

    except Exception as e:
        logging.error(f"⚠️ Kļūda ģenerēšanas laikā: {e}")
        return {"error": str(e)}
