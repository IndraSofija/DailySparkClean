from fastapi import Request
from fastapi.responses import JSONResponse
from db import get_user_by_id

async def user_info(request: Request):
    user_id = request.query_params.get("user_id")

    if not user_id:
        return JSONResponse(content={"error": "user_id is required"}, status_code=400)

    user = await get_user_by_id(user_id)
    if not user:
        return JSONResponse(content={"error": "User not found"}, status_code=404)

    return {
        "user_id": user.get("user_id"),
        "subscription_level": user.get("subscription_level", "free")
    }
