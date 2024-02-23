from typing import List
from fastapi import APIRouter

from api_v1.addresses.schemas import LegalAddress

router = APIRouter(tags=["Addresses"], prefix="/api/v1/shortest_path/addresses")


@router.post("/", description="Получить юридические адреса")
async def get_address(part_address: LegalAddress) -> LegalAddress:
    pass
