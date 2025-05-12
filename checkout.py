# checkout.py
from fastapi import APIRouter, Request
import stripe
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@router.post("/create-checkout-session")
async def create_checkout_session(request: Request):
    try:
        data = await request.json()
        plan = data.get("plan", "basic")  # <- Noklusēti "basic", ja nav norādīts

        if plan == "pro":
            price_id = os.getenv("STRIPE_PRO_PRICE_ID")
        else:
            price_id = os.getenv("STRIPE_BASIC_PRICE_ID")

        if not price_id:
            return {"error": "Price ID is not configured in environment variables."}

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            mode="subscription",  # Vai "payment" ja nav abonements
            success_url="https://dailyspark-frontend.vercel.app/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://dailyspark-frontend.vercel.app/cancel",
            client_reference_id=user_id,
        )

        return {"checkout_url": checkout_session.url}

    except Exception as e:
        return {"error": str(e)}
