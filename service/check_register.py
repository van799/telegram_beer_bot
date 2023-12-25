from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message, CallbackQuery

from config_data.config import app_settings
from database.models import User
from repository.repository_user import RepositoryUser


class RegisterUser:
    def __init__(self, message: Message | CallbackQuery, session: AsyncSession):
        self.__id = message.from_user.id
        self.__name = message.from_user.first_name
        self.__session = session

    async def check_register(self):
        repository_user = RepositoryUser(self.__session)
        if await repository_user.get_by_telegram_id(self.__id) is None:
            return False
        return True

    async def register(self):
        repository_user = RepositoryUser(self.__session)
        user = User()
        if await repository_user.get_by_telegram_id(self.__id) is None:
            user.telegram_id = self.__id
            user.first_name = self.__name
            await repository_user.add(user)
