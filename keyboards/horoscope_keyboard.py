from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.zodiac_signs import zodiac_signs


def zodiac_kb():
    """ Клавиатура всех знаков зодиака """
    kb = InlineKeyboardBuilder()
    kb.button(text='Запуск гороскопа', callback_data='start_horo')
    for zodiac in zodiac_signs:
        kb.button(text=zodiac, callback_data=f'zodiac_{zodiac}')

    kb.button(text='⬅️ Назад', callback_data='back_to_menu')
    kb.adjust(1, 4)
    return kb.as_markup()
