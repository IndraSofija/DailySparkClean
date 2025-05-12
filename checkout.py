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
        plan = data.get("plan", "basic")  # 👉 pēc noklusējuma basic, ja nav norādīts

        # ✅ Izvēlies cenu pēc plāna
        if plan == "pro":
            price_id = os.getenv("STRIPE_PRO_PRICE_ID")
        else:
            price_id = os.getenv("STRIPE_BASIC_PRICE_ID")

        if
