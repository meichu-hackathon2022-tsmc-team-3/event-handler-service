from re import A
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def heck_health():
    return {
        "detail": "OK"
    }