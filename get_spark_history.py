from fastapi import APIRouter, HTTPException
from db import get_spark_collection
from datetime import datetime

router = APIRouter()

@router.get("/user/sparks")
async def get_user_sparks(user_id: str):
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required.")

    spark_collection = get_spark_collection()
    cursor = spark_collection.find({"user_id": user_id}).sort("timestamp", -1).limit(100)
    sparks = await cursor.to_list(length=100)

  return [
    {
        "text": spark.get("spark_text", ""),
        "date": spark.get("timestamp").strftime("%Y-%m-%d %H:%M:%S") if spark.get("timestamp") else "Nav datuma"
    }
    for spark in sparks
]

