from fastapi import APIRouter, Depends

from api_v1.auth import utils as auth_utils
from api_v1.auth.schemas import TokenInfo
from app.models import User
from utils import auth

router = APIRouter(tags=["Auth"], prefix="/api/v1/shortest_path/auth")


@router.post("/login")
async def log_in(user: User = Depends(auth_utils.check_user)):
    jwt_payload: dict = {
        "sub": user.id,
        "username": user.username,
        "email": user.email,
    }
    access_token = auth.encode_jwt(jwt_payload)
    return TokenInfo(access_token=access_token, token_type="Bearer")
