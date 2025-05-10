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

