from fastapi import APIRouter, HTTPException
from datetime import datetime
from db import get_user_by_id, get_spark_collection

router = APIRouter()

@router.post("/save-spark")
async def save_spark(data: dict):
    try:
        user_id = data.get("user_id")
        spark_text = data.get("spark_text")

        if not user_id or not spark_text:
            raise HTTPException(status_code=400, detail="user_id and spark_text are required")

        user = await get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        collection = get_spark_collection()
            spark_data = {
            "user_id": user_id,
            "spark_text": spark_text,
            "timestamp": datetime.utcnow()
        }

        await collection.insert_one(spark_data)
        return {"message": "Spark saved successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
