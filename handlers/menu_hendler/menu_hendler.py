from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from config_data.config import app_settings
from database.models import User
from keyboards.keyboards import navigation_kb

from lexicon.lexicon import LEXICON_MENU
from repository.repository_user import RepositoryUser
from state_machine.admin_pass import FsmAdminForm

router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message, session: AsyncSession):
    repository_user = RepositoryUser(session)
    user = User()
    if await repository_user.get_by_telegram_id(message.from_user.id) is None:
        user.telegram_id = message.from_user.id
        await repository_user.add(user)
    await message.answer(LEXICON_MENU[message.text], reply_markup=navigation_kb)


# Этот хэндлер будет срабатывать на команду "/menu"
@router.message(Command(commands='menu'))
async def process_menu_command(message: Message):
    await message.answer(LEXICON_MENU[message.text], reply_markup=navigation_kb)


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON_MENU[message.text])


# Этот хэндлер будет срабатывать на команду "/admin"
@router.message(Command(commands='admin'), StateFilter(default_state))
async def process_help_command(message: Message, state: FSMContext):
    await message.answer("Введите пароль администратора:")
    await state.set_state(FsmAdminForm.wait_pass)


# Этот хэндлер будет срабатывать, если введенн пароль
@router.message(StateFilter(FsmAdminForm.wait_pass))
async def process_add_name(message: Message, session: AsyncSession, state: FSMContext):
    if message.text in app_settings.admin_pass:
        repository_user = RepositoryUser(session)
        user = await repository_user.get_by_telegram_id(int(message.from_user.id))
        user.admin = True
        await repository_user.add(user)
        await message.answer("Вы стали администратором:")
    else:
        await message.answer("Пароль не верный")
    await state.clear()
