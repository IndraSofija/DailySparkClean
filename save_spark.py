from fastapi import APIRouter, HTTPException
from datetime import datetime
from db import get_user_by_id, get_spark_collection

router = APIRouter()

@router.post("/save-spark")
async def save_spark(data: dict):
    try:
        user_id = data.get("user_id")
        spark_text = data.get("spark_text")

        # 1. Validācija: tukšs vai tikai atstarpes
        if not spark_text or not spark_text.strip():
            raise HTTPException(status_code=400, detail="Spark text cannot be empty.")

        # 2. Lietotājs no DB
        user = await get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Lietotājs nav atrasts.")

        # 3. Tikai Pro drīkst saglabāt
        if user.get("subscription_level") != "pro":
            raise HTTPException(status_code=403, detail="Tikai Pro lietotāji var saglabāt dzirksteles.")

        # 4. Saglabā dzirksteli
        spark_collection = get_spark_collection()
        insert_result = await spark_collection.insert_one({
            "user_id": user_id,
            "spark_text": spark_text,
            "timestamp": datetime.utcnow()
        })

        return {
            "status": "success",
            "id": str(insert_result.inserted_id)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kļūda saglabājot dzirksteli: {str(e)}")
