from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api_v1.addresses import crud
from api_v1.addresses.schemas import LegalAddress
from configs.database import get_session_dependency

router = APIRouter(tags=["Addresses"], prefix="/api/v1/shortest_path/addresses")


@router.post("/", description="Получить юридические адреса")
async def get_address_by_part(
        part_address: LegalAddress,
        session: Session = Depends(get_session_dependency),
):
    return crud.get_address_by_part(session, part_address)
