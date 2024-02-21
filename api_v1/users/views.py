from fastapi import APIRouter

router = APIRouter(tags=["Users"], prefix="/api/v1/shortest_path/users")


@router.post("/", description="Создать пользователя")
async def get_():
    pass


@router.delete("/{user_id}/", description="Удалить пользователя")
async def delete_user(user_id: int):
    pass


@router.get("/{user_id}/", description="Получить пользователя по идентификатору")
async def get_user(user_id: int):
    pass


@router.put("/{user_id}/", description="Редактировать пользователя")
async def update_user(user_id: int):
    pass
