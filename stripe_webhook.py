from fastapi import APIRouter, Request, HTTPException
import stripe
import os
from dotenv import load_dotenv
from db import get_database

load_dotenv()
router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception:
        raise HTTPException(status_code=400, detail="Webhook error")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session.get("client_reference_id")

        if user_id:
            db = get_database()
            await db["users"].update_one(
                {"user_id": user_id},
                {"$set": {"subscription_level": "pro"}}
            )
            print(f"🔁 Lietotājam {user_id} piešķirts 'pro' līmenis!")

    return {"status": "success"}
