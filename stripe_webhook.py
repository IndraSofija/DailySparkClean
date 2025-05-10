from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import stripe
import os
from dotenv import load_dotenv
from db import get_user_by_id, get_database

load_dotenv()

router = APIRouter()

# Stripe Webhook Secret
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# Webhook route
@router.post("/stripe-webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

@router.post("/stripe-webhook")
async def stripe_webhook(request: Request):

    # Apstrādājam tikai checkout.session.completed
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Iegūstam user_id no metadata
        user_id = session.get("metadata", {}).get("user_id")
        if not user_id:
            return JSONResponse(status_code=400, content={"error": "user_id nav metadata"})

        # Atjaunojam subscription_level uz "pro"
        db = get_database()
        result = await db["users"].update_one(
            {"user_id": user_id},
            {"$set": {"subscription_level": "pro"}}
        )

        print(f"✅ Lietotājs {user_id} atjaunots uz PRO. Mongo update rezultāts: {result.modified_count}")

    return {"status": "success"}
