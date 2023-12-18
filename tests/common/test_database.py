import os
import time

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from database.models import Base


# from tests.common.test_models import Base


class TestDatabase:
    def __init__(self):
        self.path = f'sql_app_{hash(time.time())}.db'
        self.SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///./{self.path}"
        self.engine = create_async_engine(
            self.SQLALCHEMY_DATABASE_URL, echo=True, future=True
        )
        self.async_session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def create_session(self):
        await self.metadate_create_all()
        return AsyncSession(self.engine)

    async def metadate_create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    def remove_database_file(self):
        if os.path.exists(self.path):
            os.remove(self.path)
