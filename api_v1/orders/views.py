
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api_v1.auth.utils import get_current_user
from api_v1.orders import crud
from api_v1.orders.schemas import OrderCreate
from app.models import User
from configs.database import get_session_dependency

router = APIRouter(tags=["Orders"], prefix="/api/v1/shortest_path/orders")


@router.get("/", description="")
async def get(
    _: User = Depends(get_current_user),
    session: Session = Depends(get_session_dependency),
):
    return crud.get_orders(session)


@router.post("/", description="")
async def crate(
    order: OrderCreate,
    _: User = Depends(get_current_user),
    session: Session = Depends(get_session_dependency),
):
    return crud.create(session, order)


@router.delete("/{order_id}/", description="")
async def delete(
    order_id: int,
    _: User = Depends(get_current_user),
    session: Session = Depends(get_session_dependency),
):
    order = crud.get_order(session, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Executor with {order_id=} not found",
        )

    return crud.delete(session, order)
