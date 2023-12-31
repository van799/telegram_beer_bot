from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, PhotoSize, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Beer, User
from filters.chat_type import ChatTypeFilter
from filters.filters import IsDigitCallbackData, IsDelBookmarkCallbackData
from keyboards.inline_keyboards import create_beers_keyboard, create_delete_keyboard

from lexicon.lexicon import LEXICON, LEXICON_MENU
from repository.repository_beer import RepositoryBeer
from repository.repository_user import RepositoryUser
from service.check_register import RegisterUser
from state_machine.add_beer import FsmBeerForm

router = Router()


# Этот хэндлер будет срабатывать на команду add_beer вне состояний
# и предлагать перейти к добовлению пива

@router.message(ChatTypeFilter(chat_type=["private"]), F.text == LEXICON['add_beer'], StateFilter(default_state))
async def process_add_beer_command(message: Message, state: FSMContext, session: AsyncSession):
    register_user = RegisterUser(message, session)
    if await register_user.check_register() is False:
        await message.answer(LEXICON['not_user'])
    else:
        await message.answer(LEXICON['add_name'])
        # Устанавливаем состояние ожидания ввода имени
        await state.set_state(FsmBeerForm.add_name)


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@router.message(ChatTypeFilter(chat_type=["private"]), Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text=LEXICON['cancel_null']
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(ChatTypeFilter(chat_type=["private"]), Command(commands='cancel'), ~StateFilter(default_state))
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
    await message.answer(text=LEXICON['sort_beer'])
    # Устанавливаем состояние ожидания выбора образования
    await state.set_state(FsmBeerForm.sort_beer)


@router.message(StateFilter(FsmBeerForm.sort_beer))
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


@router.message(StateFilter(FsmBeerForm.rating),
                lambda x: x.text.isdigit() and 0 <= int(x.text) <= 10)
async def process_rating(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "rating"
    await state.update_data(rating=message.text)
    await message.answer(text=LEXICON['price'])
    # Устанавливаем состояние ожидания ввода изображения
    await state.set_state(FsmBeerForm.price)


# Этот хэндлер будет срабатывать, введен неверный рейтинг
@router.message(StateFilter(FsmBeerForm.rating))
async def warning_rating(message: Message):
    await message.answer(
        text=LEXICON['warning_rating']
    )


@router.message(StateFilter(FsmBeerForm.price),
                lambda x: x.text.isdigit() and 0 <= int(x.text) <= 10000)
async def process_price(message: Message, state: FSMContext, session: AsyncSession):
    # Cохраняем введенное имя в хранилище по ключу "price"
    await state.update_data(price=message.text)
    await state.set_state(FsmBeerForm.rating)

    repository_user = RepositoryUser(session)
    repository_beer = RepositoryBeer(session)

    beer = Beer()
    user_result = await repository_user.get_by_telegram_id(message.from_user.id)

    beer.user_id = user_result.id
    data = await state.get_data()
    beer.price = data['price']
    beer.photo_id = data['photo_id']
    beer.rating = data['rating']
    beer.name = data['add_name']
    beer.comment = data['comment']
    beer.sort_beer_id = 1

    await repository_beer.add(beer)

    # Завершаем машину состояний
    await state.clear()
    await message.answer(text=LEXICON['save_beer'])


@router.message(StateFilter(FsmBeerForm.price))
async def warning_rating(message: Message):
    await message.answer(
        text=LEXICON['warning_price']
    )


@router.message(F.text == LEXICON['view_beer'])
async def process_view_beer(message: Message, session: AsyncSession):
    register_user = RegisterUser(message, session)
    if await register_user.check_register() is False:
        await message.answer(LEXICON['not_user'])
    else:
        # Отправляем пользователю инофрмацию, если она есть в "базе данных"
        repository_beer = RepositoryBeer(session)
        repository_user = RepositoryUser(session)
        result_beers = await repository_beer.get_all()

        if not result_beers:
            # Если данных в базе нет
            await message.answer(
                text=LEXICON['not_beer']
            )
        else:
            name_beers = {}
            for beer in result_beers:
                user: User = await repository_user.get_by_id(beer.user_id)
                beer_name = f'{beer.name}. Цена: {beer.price} руб. Добавил {user.first_name}'
                name_beers.update({beer.id: beer_name})
            await message.answer(
                text=LEXICON['list_beer'],
                reply_markup=create_beers_keyboard(name_beers))


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с названием напитка из списка
@router.callback_query(IsDigitCallbackData())
async def process_beer_press(callback: CallbackQuery, session: AsyncSession):
    register_user = RegisterUser(callback, session)
    if await register_user.check_register() is False:
        await callback.answer(LEXICON['not_user'])
    else:
        repository_beer = RepositoryBeer(session)
        beer = await repository_beer.get_by_id(int(callback.data))
        await callback.message.answer_photo(
            photo=beer.photo_id,
            caption=f'Название: {beer.name}\n'
                    f'Сорт напитка: {beer.sort_beer_id}\n'
                    f'отзыв: {beer.comment}\n'
                    f'Рейтинг: {beer.rating}\n'
                    f'Цена: {beer.price}'
        )


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком закладок
@router.callback_query(F.data == 'delete')
async def process_delete_press(callback: CallbackQuery, session: AsyncSession):
    register_user = RegisterUser(callback, session)
    if await register_user.check_register() is False:
        await callback.answer(LEXICON['not_user'])
    else:
        repository_beer = RepositoryBeer(session)
        result_beers = await repository_beer.get_all()
        name_beers = {}
        for beer in result_beers:
            beer_name = f'{beer.name}. Цена: {beer.price} руб.'
            name_beers.update({beer.id: beer_name})
        await callback.message.edit_text(
            text=LEXICON[callback.data],
            reply_markup=create_delete_keyboard(name_beers)
        )
        await callback.answer()


@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel'])
    await callback.answer()


@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_beer_press(callback: CallbackQuery, session: AsyncSession):
    register_user = RegisterUser(callback, session)
    if await register_user.check_register() is False:
        await callback.answer(LEXICON['not_user'])
    else:
        repository_beer = RepositoryBeer(session)
        repository_user = RepositoryUser(session)
        user = await repository_user.get_by_telegram_id(callback.from_user.id)
        beer = await repository_beer.get_by_id(callback.data[:-3])
        if user.id == beer.user_id or user.admin is True:
            await repository_beer.delete_by_id(int(callback.data[:-3]))
            result_beers = await repository_beer.get_all()
            name_beers = {}
            for beer in result_beers:
                beer_name = f'{beer.name}. Цена: {beer.price} руб.'
                name_beers.update({beer.id: beer_name})
            await callback.message.edit_text(
                text=LEXICON['list_beer'],
                reply_markup=create_delete_keyboard(name_beers)
            )
        else:
            await callback.answer(text='Удалить можно только свой добавленый напиток')
