# checkout.py
from fastapi import APIRouter, Request, HTTPException
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
        user_id = data.get("user_id")
        plan = data.get("plan", "basic")  # noklusēti "basic"

        if not user_id:
            raise HTTPException(status_code=400, detail="Missing user_id")

        # Izvēlamies pareizo cenu
        if plan == "pro":
            price_id = os.getenv("STRIPE_PRO_PRICE_ID")
        else:
            price_id = os.getenv("STRIPE_BASIC_PRICE_ID")

        if not price_id:
            raise HTTPException(status_code=500, detail="Price ID not configured")

        # Izveidojam Checkout sesiju
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            mode="subscription",  # vai "payment", ja nevēlies recurring
            success_url="https://dailyspark-frontend.vercel.app/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://dailyspark-frontend.vercel.app/cancel",
            client_reference_id=user_id,         # ← šī rinda!
        )

        return {"checkout_url": checkout_session.url}

    except HTTPException as he:
        raise he
    except Exception as e:
        # drošs kļūdas gaiss
        raise HTTPException(status_code=500, detail=str(e))
