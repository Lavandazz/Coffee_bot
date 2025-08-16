from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.zodiac_signs import zodiac_signs


def zodiac_kb():
    """ Клавиатура всех знаков зодиака """
    kb = InlineKeyboardBuilder()
    for zodiac in zodiac_signs:
        kb.button(text=zodiac, callback_data=f'zodiac_{zodiac}')

    kb.adjust(4)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))

    return kb.as_markup()
