import asyncio

from sqlalchemy import text

from configs.database import session_factory, async_session_factory


async def get_version():
    async with async_session_factory() as session:
        res = await session.execute(text("SELECT VERSION();"))
        print(f"{res.first()=}")


if __name__ == "__main__":
    with session_factory() as session:
        res = session.execute(text("SELECT VERSION();"))
        print(f"{res.first()=}")

    asyncio.get_event_loop().run_until_complete(get_version())
