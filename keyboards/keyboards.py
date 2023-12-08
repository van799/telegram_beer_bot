from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON

# ------- Создаем клавиатуру через ReplyKeyboardBuilder -------

# Создаем кнопки с ответами согласия и отказа
button_view_beer = KeyboardButton(text=LEXICON['view_beer'])
button_search = KeyboardButton(text=LEXICON['search'])
button_add_beer = KeyboardButton(text=LEXICON['add_beer'])

# Инициализируем билдер для клавиатуры с кнопками
navigation_kb_builder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер
navigation_kb_builder.row(button_view_beer,
                          button_search,
                          button_add_beer,
                          width=1)

navigation_kb: ReplyKeyboardMarkup = navigation_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)
