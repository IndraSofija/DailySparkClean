# db.py
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
database = client["daily_spark"]

def get_database():
    return database

async def get_user_by_id(user_id: str):
    db = get_database()
    print("🔍 Meklējam user_id:", repr(user_id))
    print("🧮 Rakstzīmju garums:", len(user_id), "| Tips:", type(user_id))
    user = await db["users"].find_one({"user_id": user_id})
    print("👁️ Mongo rezultāts:", user)
    return user

def get_spark_collection():
    db = get_database()
    return db["saved_sparks"]

def get_user_collection():
    db = get_database()
    return db["users"]

async def update_user_spark_data(user_id, sparks_used_today=None, last_reset_date=None):
    db = get_database()
    user_collection = db["users"]

    update_fields = {}
    if sparks_used_today is not None:
        update_fields["sparks_used_today"] = sparks_used_today
    if last_reset_date is not None:
        update_fields["last_reset_date"] = last_reset_date

    if update_fields:
        await user_collection.update_one(
            {"user_id": user_id},
            {"$set": update_fields},
            upsert=True
        )
