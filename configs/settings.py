import enum
import os

from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()

BASE_DIR = Path(__file__).parent.parent


class Status(enum.Enum):
    pending = "pending"
    done = "done"
    canceled = "canceled"


class Category(enum.Enum):
    lightweight = "lightweight"
    heavy = "heavy"


class Transport(enum.Enum):
    auto = "auto"
    mt = "mt"
    pd = "pd"
    bc = "bc"
    sc = "sc"


class AuthJWT(BaseModel):
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 20


class Settings(BaseSettings):
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = os.getenv("DB_PORT")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    DB_NAME: str = os.getenv("DB_NAME")

    @property
    def DATABASE_URL_asyncpg(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
