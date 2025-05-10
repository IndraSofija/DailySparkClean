from fastapi import APIRouter, HTTPException
from datetime import datetime
from db import get_user_by_id, get_spark_collection, update_user_spark_data

router = APIRouter()

@router.post("/save-spark")
async def save_spark(data: dict):
    user_id = data.get("user_id")
    spark_text = data.get("spark_text")

    if not user_id or not spark_text:
        raise HTTPException(status_code=400, detail="user_id and spark_text are required.")

    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    today = datetime.utcnow().date()
    last_reset_str = user.get("last_reset_date")
    try:
        last_reset_date = datetime.strptime(last_reset_str, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        last_reset_date = None


    # Ja nav šodienas datums — reset
    if last_reset_date != today:
        await update_user_spark_data(user_id, sparks_used_today=1, last_reset_date=today.isoformat())
    else:
        sparks_used = user.get("sparks_used_today", 0)
        subscription = user.get("subscription_level", "free")

        # Limits pēc līmeņa
        if subscription == "free" and sparks_used >= 1:
            return {"error": "Spark limit reached. Try again tomorrow."}
        elif subscription == "basic" and sparks_used >= 3:
            return {"error": "Spark limit reached. Try again tomorrow."}
        elif subscription == "pro" and sparks_used >= 5:
            return {"error": "Spark limit reached. Try again tomorrow."}

        await update_user_spark_data(user_id, sparks_used_today=sparks_used + 1)

    # Saglabāt dzirksteli
    spark_collection = await get_spark_collection()
    await spark_collection.insert_one({
        "user_id": user_id,
        "spark_text": spark_text,
        "timestamp": datetime.utcnow()
    })

    return {"message": "Spark saved successfully."}
