from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from config_data.config import app_settings
from database.models import User
from filters.chat_type import ChatTypeFilter
from keyboards.keyboards import navigation_kb

from lexicon.lexicon import LEXICON_MENU, LEXICON_TEXT, LEXICON
from repository.repository_user import RepositoryUser
from service.check_register import RegisterUser
from service.register_admin import RegisterAdmin
from state_machine.admin_pass import FsmAdminForm

router = Router()
router.message.filter(
    ChatTypeFilter(chat_type=["private"])
)


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message, session: AsyncSession):
    register_user = RegisterUser(message, session)
    if await register_user.check_register() is False:
        await register_user.register()
        await message.answer(LEXICON_TEXT[message.text[0:6]], reply_markup=navigation_kb)
    else:
        await message.answer(LEXICON['already_authorized'], reply_markup=navigation_kb)


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message, session: AsyncSession):
    register_user = RegisterUser(message, session)
    if await register_user.check_register() is False:
        await message.answer(LEXICON['not_user'])
    else:
        await message.answer(LEXICON_TEXT[message.text[0:5]])


# Этот хэндлер будет срабатывать на команду "/admin"
@router.message(Command(commands='admin'), StateFilter(default_state))
async def process_help_command(message: Message, state: FSMContext, session: AsyncSession):
    register_user = RegisterUser(message, session)
    register_admin = RegisterAdmin(message, session)
    if await register_user.check_register() is False:
        await message.answer(LEXICON['not_user'])
    elif await register_admin.check_admin() is True:
        await message.answer(LEXICON['admin'])
    else:
        await message.answer(LEXICON['input_password'])
        await state.set_state(FsmAdminForm.wait_pass)


# Этот хэндлер будет срабатывать, если введенн пароль
@router.message(StateFilter(FsmAdminForm.wait_pass))
async def process_admin_authorization(message: Message, session: AsyncSession, state: FSMContext):
    register_admin = RegisterAdmin(message, session)
    result_admin_authorization = await register_admin.authorization_admin(message.text)
    if result_admin_authorization is True:
        await message.answer(LEXICON['admin_successful'])
    else:
        await message.answer(LEXICON['wrong_password'])
    await state.clear()
