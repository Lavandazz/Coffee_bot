from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.config import SUPERADMIN
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


def admin_kb():
    """ Кнопки в отделе администрирования """
    kb = InlineKeyboardBuilder()
    kb.button(text="Статистика",
              callback_data="statistic")
    kb.button(text="Управление правами",
              callback_data="rights")
    if SUPERADMIN:
        kb.row(InlineKeyboardButton(text='Запуск гороскопа', callback_data='start_horo'))
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))

    return kb.as_markup()


def admin_stat_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='За день', callback_data='stat_day')
    kb.button(text='За период', callback_data='stat_all')
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
    return kb.as_markup()

