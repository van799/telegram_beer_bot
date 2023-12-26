from aiogram.fsm.state import StatesGroup, State


class FsmSearchForm(StatesGroup):
    wait_search = State()     # Состояние ожидания ввода пароля
