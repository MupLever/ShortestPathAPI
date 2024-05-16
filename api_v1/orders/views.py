import json
from datetime import datetime

# import pandas as pd
from starlette import status
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, UploadFile

from api_v1.auth.utils import get_current_user
from api_v1.orders import crud
from api_v1.orders.schemas import OrderCreate
from app.models import User
from configs.database import get_session_dependency
from app.types import Category, Status

router = APIRouter(tags=["Orders"], prefix="/api/v1/shortest_path/orders")


@router.get("/", description="")
async def get_orders(
    date: datetime,
    category: Category,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session_dependency),
):
    return crud.get_orders(session, user, date, category)


@router.post("/", description="")
async def create(
    order: OrderCreate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session_dependency),
):
    order_dict = order.model_dump()
    return crud.create(session, user, order_dict)


@router.post("/file/", description="")
async def create(
    file: UploadFile,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session_dependency),
):
    order_dict = (
        json.load(file.file)
        # pd.read_excel(file.file).to_dict()
        if file.filename.endswith(".xlsx")
        else json.load(file.file)
    )
    if isinstance(order_dict, list):
        for order in order_dict:
            crud.create(session, user, order_dict=order)
    else:
        crud.create(session, user, order_dict=order_dict)

    return {"message": "The file was sent successfully"}


@router.post("/{order_id}/", description="")
async def update_status(
        order_id: int,
        order_status: Status,
        user: User = Depends(get_current_user),
        session: Session = Depends(get_session_dependency)
):
    order = crud.get_order(session, user, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Executor with {order_id=} not found",
        )

    return crud.update_status(session, order, order_status)
