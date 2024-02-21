from typing import List
from fastapi import APIRouter


router = APIRouter(tags=["Addresses"], prefix="/api/v1/shortest_path/addresses")


@router.post("/", description="Получить юридические адреса")
async def get_address():
    pass
