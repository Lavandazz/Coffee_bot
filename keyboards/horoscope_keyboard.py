from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.zodiac_signs import zodiac_signs
from utils.config import SUPERADMIN
from utils.logging_config import bot_logger


def zodiac_kb():
    """ Клавиатура всех знаков зодиака """
    kb = InlineKeyboardBuilder()
    for zodiac in zodiac_signs:
        kb.button(text=zodiac, callback_data=f'zodiac_{zodiac}')

    kb.adjust(4)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
    if SUPERADMIN:
        kb.row(InlineKeyboardButton(text='Запуск гороскопа', callback_data='start_horo'))
    bot_logger.debug(f'передаю клавы {list(kb.buttons)}')
    return kb.as_markup()
