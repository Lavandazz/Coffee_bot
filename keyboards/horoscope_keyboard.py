from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.zodiac_signs import zodiac_signs


def zodiac_kb():
    """ Клавиатура всех знаков зодиака """
    kb = InlineKeyboardBuilder()
    for zodiak in zodiac_signs:
        kb.button(text=zodiak, callback_data=zodiak)

    kb.adjust(4)
    return kb.as_markup()
