from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import LEXICON
from repository.repository_beer import RepositoryBeer
from service.check_register import RegisterUser
from state_machine.search_beer import FsmSearchForm

router = Router()


@router.message(F.text == LEXICON['search'], StateFilter(default_state))
async def process_search_beer_command(message: Message, state: FSMContext, session: AsyncSession):
    register_user = RegisterUser(message, session)
    if await register_user.check_register() is False:
        await message.answer(LEXICON['not_user'])
    else:
        await message.answer(LEXICON['search_name'])
        await state.set_state(FsmSearchForm.wait_search)


@router.message(StateFilter(FsmSearchForm.wait_search))
async def process_search_beer(message: Message, session: AsyncSession, state: FSMContext):
    repository_beer = RepositoryBeer(session)
    result_search = await repository_beer.search_name(str(message.text))
    if result_search is None:
        await message.answer(LEXICON['not_search'])
    else:
        await message.answer_photo(
            photo=result_search.photo_id,
            caption=f'Название: {result_search.name}\n'
                    f'Сорт напитка: {result_search.sort_beer_id}\n'
                    f'отзыв: {result_search.comment}\n'
                    f'Рейтинг: {result_search.rating}\n'
                    f'Цена: {result_search.price}'
        )

    await state.clear()
