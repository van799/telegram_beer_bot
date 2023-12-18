from abc import ABC, abstractmethod

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Base, User, Beer
from repository.repository_base import RepositoryBase


class RepositoryBeer(RepositoryBase):
    """Класс репозитория для работы с Beer в БД."""

    def __init__(self, session):
        super().__init__(session, Beer)

    async def get_all(self):
        result = await self.session.scalars(select(Beer))
        return result.all()
