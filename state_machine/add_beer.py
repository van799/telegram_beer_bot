from aiogram.fsm.state import StatesGroup, State


class FsmBeerForm(StatesGroup):
    add_name = State()     # Состояние ожидания ввода названия пиво
    upload_photo = State()  # Состояние ожидания загрузки фото
    sort_beer = State()    # Состояние ожидания сорт пиво
    comment = State()       # Состояние ожидания отзыв
    rating = State()        # Состояние ожидания рейтинг
    price = State()         # Состояние ожидания цена
