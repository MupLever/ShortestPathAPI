from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from configs.database import get_session_dependency
from configs.orm import get_address_by_part

router = APIRouter(tags=["Addresses"], prefix="/api/v1/shortest_path/addresses")


@router.get("/", description="Получить юридические адреса")
async def get_address_by(
    part_address: str,
    session: Session = Depends(get_session_dependency),
):
    return get_address_by_part(session, part_address)
