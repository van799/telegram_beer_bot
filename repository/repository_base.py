from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Base


class RepositoryBase(ABC):
    """
        Абстрактный класс реализует базовый функционал работы
        с базой данных.
    """

    def __init__(self, session: AsyncSession, repository_type: type(Base)):
        self.session = session
        self.repository_type = repository_type

    @abstractmethod
    def add(self, model):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def update_by_id(self):
        pass

    @abstractmethod
    def delete(self):
        pass
