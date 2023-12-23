from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


# Функция, генерирующая клавиатуру для отображения и редактирования записи
def create_beers_keyboard(args: dict) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for key, value in args.items():
        kb_builder.row(InlineKeyboardButton(
            text=f'{key} - {value}',
            callback_data=str(key)
        ))
    # Добавляем в клавиатуру в конце две кнопки "Редактировать"
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['delete'],
            callback_data='delete'
        ),
        width=1
    )
    return kb_builder.as_markup()


def create_delete_keyboard(args: dict) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками
    for key, value in args.items():
        kb_builder.row(InlineKeyboardButton(
            text=f'{LEXICON["del"]} {key} - {value}',
            callback_data=f'{key}del'
        ))
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['cancel'],
            callback_data='cancel'
        ),
        width=1
    )
    return kb_builder.as_markup()

