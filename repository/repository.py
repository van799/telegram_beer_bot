import asyncio
from abc import ABC

from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import Database
from database.modes import User


class RepositoryUser(ABC):
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add(self) -> None:
        user = User(telegram_id=1513)

        telegram_id: Mapped[int] = mapped_column(String(64))
        async with self.__session.begin():
           # await self.__session.add(user)
            self.__session.add(user)


database = Database()
repository = RepositoryUser(database.async_session)
asyncio.run(repository.add())
