from fastapi import APIRouter
from app.types import Category

router = APIRouter(tags=["Categories"], prefix="/api/v1/shortest_path/categories")


@router.get("/", description="")
async def get_categories():
    return [category.value for category in Category]
