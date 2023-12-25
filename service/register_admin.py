from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message, CallbackQuery

from config_data.config import app_settings
from repository.repository_user import RepositoryUser


class RegisterAdmin:
    def __init__(self, message: Message | CallbackQuery, session: AsyncSession):
        self.__id = message.from_user.id
        self.__session = session

    async def check_admin(self):
        repository_user = RepositoryUser(self.__session)
        user = await repository_user.get_by_telegram_id(self.__id)
        if user.admin is True:
            return True
        return False

    async def authorization_admin(self, password):
        if password == app_settings.admin_pass:
            repository_user = RepositoryUser(self.__session)
            user = await repository_user.get_by_telegram_id(self.__id)
            user.admin = True
            await repository_user.add(user)
            return True
        return False
