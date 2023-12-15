from abc import ABC, abstractmethod

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Base, User
from repository.repository_base import RepositoryBase


class RepositoryUser(RepositoryBase):
    """Класс репозитория для работы с User в БД."""

    def __init__(self, session):
        super().__init__(session, User)

    async def get_by_telegram_id(self, tg_id):
        result = await self.session.scalar(select(User).filter(User.telegram_id == tg_id))
        return result
