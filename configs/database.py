from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from configs.settings import settings

engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False,
    pool_size=5,
    max_overflow=10,
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
    pool_size=5,
    max_overflow=10,
)

session_factory = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_session_dependency():
    with session_factory() as session:
        yield session
