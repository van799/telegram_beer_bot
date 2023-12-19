import asyncio
import time

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config_data.config import app_settings
from database.models import Base


class Database:
    def __init__(self, ):
        if app_settings.debug == True:
            self.path = f'sql_app_{hash(time.time())}.db'
            self.SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///./{self.path}"

        else:
            self.path = f'sql_app.db'
            self.SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///./{self.path}"

        self.engine = create_async_engine(
            self.SQLALCHEMY_DATABASE_URL, echo=True, future=True
        )
        self.async_session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def create_session(self):
        # debug=True создание новой БД, debug=False соединение с БД
        if app_settings.debug == True:
            await self.metadate_create_all()
        return AsyncSession(self.engine)

    async def metadate_create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
