from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, PhotoSize
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from keyboards.keyboards import navigation_kb

from lexicon.lexicon import LEXICON, LEXICON_MENU
from repository.repository_user import RepositoryUser
from state_machine.add_beer import FsmBeerForm

router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message, session: AsyncSession):
    repository_user = RepositoryUser(session)
    user = User()
    user.telegram_id = message.from_user.id
    await repository_user.add(user)
    result = await repository_user.get_by_telegram_id(user, message.from_user.id)
    print(result)
    # if await repository_user.get_by_telegram_id(message.from_user.id) is not None:
    #     user.telegram_id = message.from_user.id
    #     await repository_user.add(user)
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


# Этот хэндлер будет срабатывать на команду add_beer вне состояний
# и предлагать перейти к добовлению пива
@router.message(F.text == LEXICON['add_beer'], StateFilter(default_state))
async def process_add_beer_command(message: Message, state: FSMContext):
    await message.answer(LEXICON['add_name'])
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FsmBeerForm.add_name)


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text=LEXICON['cancel_add_beer']
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text=LEXICON['cancel_add_beer'])
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать, если введено  название пиво
# и переводить в состояние ожидания ввода изображения
@router.message(StateFilter(FsmBeerForm.add_name))
async def process_add_name(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(add_name=message.text)
    await message.answer(text=LEXICON['upload_photo'])
    # Устанавливаем состояние ожидания ввода изображения
    await state.set_state(FsmBeerForm.upload_photo)


@router.message(StateFilter(FsmBeerForm.upload_photo), F.photo[-1].as_('largest_photo'))
async def process_upload_photo(message: Message,
                               state: FSMContext,
                               largest_photo: PhotoSize):
    # Cохраняем данные фото (file_unique_id и file_id) в хранилище
    # по ключам "photo_unique_id" и "photo_id"
    await state.update_data(
        photo_unique_id=largest_photo.file_unique_id,
        photo_id=largest_photo.file_id
    )
    await message.answer(text=LEXICON['model_beer'])
    # Устанавливаем состояние ожидания выбора образования
    await state.set_state(FsmBeerForm.model_beer)


@router.message(StateFilter(FsmBeerForm.model_beer))
async def process_model_beer(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(model_beer=message.text)
    await message.answer(text=LEXICON['comment'])
    # Устанавливаем состояние ожидания ввода изображения
    await state.set_state(FsmBeerForm.comment)


@router.message(StateFilter(FsmBeerForm.comment))
async def process_comment(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(comment=message.text)
    await message.answer(text=LEXICON['rating'])
    # Устанавливаем состояние ожидания ввода изображения
    await state.set_state(FsmBeerForm.rating)


@router.message(StateFilter(FsmBeerForm.rating))
async def process_rating(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(rating=message.text)
    await message.answer(text=LEXICON['price'])
    # Устанавливаем состояние ожидания ввода изображения
    await state.set_state(FsmBeerForm.price)


@router.message(StateFilter(FsmBeerForm.price))
async def process_price(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(price=message.text)

    await state.set_state(FsmBeerForm.rating)

    user_dict[message.from_user.id] = await state.get_data()
    # Завершаем машину состояний
    await state.clear()
    await message.answer(text=LEXICON['save_beer'])

# Этот хэндлер будет срабатывать на отправку команды "Просмотр пива"
# @router.message(F.text == LEXICON['view_beer'], StateFilter(default_state))
# async def process_view_beer(message: Message):
#     # Отправляем пользователю инофрмацию, если она есть в "базе данных"
#     if message.from_user.id in user_dict:
#         await message.answer_photo(
#             photo=user_dict[message.from_user.id]['photo_id'],
#             caption=f'Название: {user_dict[message.from_user.id]["add_name"]}\n'
#                     f'Сорт напитка: {user_dict[message.from_user.id]["model_beer"]}\n'
#                     f'отзыв: {user_dict[message.from_user.id]["comment"]}\n'
#                     f'Рейтинг: {user_dict[message.from_user.id]["rating"]}\n'
#                     f'Цена: {user_dict[message.from_user.id]["price"]}'
#         )
#     else:
#         # Если анкеты пользователя в базе нет - предлагаем заполнить
#         await message.answer(
#             text=LEXICON['not_beer']
#         )
