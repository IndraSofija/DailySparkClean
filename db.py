# db.py
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
database = client["dailyspark"]

def get_database():
    return database

async def get_user_by_id(user_id: str):
    db = get_database()
    return await db["users"].find_one({"user_id": user_id})

def get_spark_collection():
    db = get_database()
    return db["saved_sparks"]
