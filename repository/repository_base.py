from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from database.models import Base


class RepositoryBase(ABC):
    """
        Абстрактный класс реализует базовый функционал работы
        с базой данных.
    """

    def __init__(self, session: AsyncSession, repository_type: type(Base)):
        self.session = session
        self.repository_type = repository_type

    async def add(self, model):
        self.session.add(model)
        await self.session.commit()

    async def get_by_id(self, id):
        result = await self.session.get(self.repository_type, id)
        return result

    async def delete_by_id(self, id):
        await self.session.execute(delete(self.repository_type).where(self.repository_type.id == id))
        await self.session.commit()

