from fastapi import APIRouter
from db import get_spark_collection
from datetime import datetime

router = APIRouter()

@router.post("/admin/fix-timestamps")
async def fix_missing_timestamps():
    collection = get_spark_collection()
    missing = collection.find({"timestamp": {"$exists": False}})
    count = 0
    async for doc in missing:
        await collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"timestamp": datetime.utcnow()}}
        )
        count += 1
    return {"fixed": count}
