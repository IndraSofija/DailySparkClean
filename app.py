import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

# Ielādē .env mainīgos
load_dotenv()

# Inicializē API klientu
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Izveido FastAPI instanci
app = FastAPI()

# Atļauj piekļuvi no jebkuras vietnes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Testa endpoint
@app.get("/")
async def root():
    return {"message": "DailySpark backend is running."}

# Satura ģenerēšanas endpoint
@app.post("/generate")
async def generate_content(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content.strip()
        return {"result": result}
    except Exception as e:
        logging.error(f"Kļūda: {e}")
        return {"error": str(e)}
