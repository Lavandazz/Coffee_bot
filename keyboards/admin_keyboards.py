from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.logging_config import bot_logger


def admin_btn(role: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="Бариста",
              callback_data="barista")
    if role == "admin":
        kb.button(text="Админ",
                  callback_data="admin")

    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))

    return kb.as_markup()


def admin_keyboard():
    """ Кнопки в отделе администрирования """
    kb = InlineKeyboardBuilder()
    kb.button(text="Статистика за день",
              callback_data="statistic")
    kb.button(text="Управление правами",
              callback_data="rights")
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))

    return kb.as_markup()


