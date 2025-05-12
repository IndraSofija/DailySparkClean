# get_saved_sparks.py
from fastapi import APIRouter, HTTPException
from db import get_spark_collection

router = APIRouter()

@router.post("/get-saved-sparks")
async def get_saved_sparks(data: dict):
    user_id = data.get("user_id")

    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id")

    collection = get_spark_collection()

    # Atrodam visas dzirksteles konkrētajam user_id
    sparks_cursor = collection.find({"user_id": user_id}).sort("timestamp", -1)
    sparks = []
    async for spark in sparks_cursor:
        sparks.append({
            "spark_text": spark.get("spark_text"),
            "timestamp": spark.get("timestamp")
        })

    return {"sparks": sparks}
