from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import openai
import os
import logging

load_dotenv()

app = FastAPI()

# CORS iestatījumi
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    return {"message": "DailySpark backend is running."}

@app.post("/generate")
async def generate_content(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        result = response.choices[0].message.content.strip()
        return {"result": result}
    
    except Exception as e:
        logger.error(f"Kļūda ģenerēšanā: {e}")
        return {"error": str(e)}
