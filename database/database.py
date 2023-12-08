import asyncio
import time

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from database.modes import Base


class Database:
    def __init__(self):
        self.path = f'sql_app_{hash(time.time())}.db'
        self.SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///./{self.path}"
        self.engine = create_async_engine(
            self.SQLALCHEMY_DATABASE_URL, echo=True, future=True
        )
        self.async_session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        asyncio.run(self.metadate_create_all())

    async def create_session(self):
        await self.metadate_create_all()
        return AsyncSession(self.engine)

    async def metadate_create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_session(self) -> AsyncSession:
        async with self.async_session() as session:
            yield session


user_dict: dict[int, dict[str, str | int | bool]] = {}
