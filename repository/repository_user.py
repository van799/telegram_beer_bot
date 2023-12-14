from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Base, User
from repository.repository_base import RepositoryBase


class RepositoryUser(RepositoryBase):
    """Класс репозитория для работы с User в БД."""

    def __init__(self, session):
        super().__init__(session, User)

    async def add(self, model):
        self.session.add(model)
        await self.session.commit()

    async def get_by_id(self, id):
        result = await self.session.get(User, id)
        return result

    async def get_by_telegram_id(self, tg_id):
        result = await self.session.execute(select(User).filter_by(telegram_id=tg_id)).all()

        return result

    async def update_by_id(self):
        pass

    async def delete(self):
        pass
