from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from pymongo import MongoClient
import os

router = APIRouter()

# Mongo savienojums
MONGO_URL = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URL)
db = client["daily_spark"]
saved_sparks = db["saved_sparks"]
users = db["users"]

# Pieprasījuma dati
class SparkSaveRequest(BaseModel):
    user_id: str
    spark_text: str

@router.post("/save-spark")
async def save_spark(request: SparkSaveRequest):
    try:
        # Meklē lietotāju DB
        user = users.find_one({"user_id": request.user_id})
        if not user:
            raise HTTPException(status_code=404, detail="Lietotājs nav atrasts.")
        if user.get("subscription_level") != "pro":
            raise HTTPException(status_code=403, detail="Tikai Pro lietotāji var saglabāt dzirksteles.")

        # Saglabā dzirksteli
        spark = {
            "user_id": request.user_id,
            "spark_text": request.spark_text,
            "timestamp": datetime.utcnow()
        }
        result = saved_sparks.insert_one(spark)
        return {"status": "success", "id": str(result.inserted_id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kļūda saglabājot dzirksteli: {str(e)}")
