from pydantic import BaseModel


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class AuthUser(BaseModel):
    email: str
    password: str
