from aiogram.fsm.state import StatesGroup, State


class FsmAdminForm(StatesGroup):
    wait_pass = State()     # Состояние ожидания ввода пароля
