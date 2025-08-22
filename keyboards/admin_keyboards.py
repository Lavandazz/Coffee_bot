from typing import List

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models_db import User
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


def admin_rights():
    kb = InlineKeyboardBuilder()
    kb.button(text='Добавить админа', callback_data='add_admin')
    kb.button(text='Удалить админа', callback_data='admins_for_delete')
    kb.button(text='Добавить бариста', callback_data='add_barista')
    kb.button(text='Удалить бариста', callback_data='baristas_for_delete')
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
    return kb.as_markup()


def yes_or_no_btn():
    kb = InlineKeyboardBuilder()
    kb.button(text='Да', callback_data='yes')
    kb.button(text='Нет', callback_data='no')
    kb.adjust(2)
    return kb.as_markup()


def admin_stat_kb():
    """Клавиатура для статистики"""
    kb = InlineKeyboardBuilder()
    kb.button(text='За день', callback_data='stat_day')
    kb.button(text='За период', callback_data='stat_all')
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
    return kb.as_markup()


async def all_baristas_or_admins_kb(users: List[User], status: str = None):
    """
    Клавиатура с пользователями, которым необходимо изменить роль.
    Если список пуст, то status не передается и отправляется только кнопка Назад.
    :param users: Юзеры как клавиатура
    :param status: Передаем строку: "delete", "baristas", "admin".
    :return: kb
    """
    kb = InlineKeyboardBuilder()
    for user in users:
        if status == "delete":
            kb.button(text=f'{user.username}', callback_data=f'delete_{user.id}')
        if status == "barista":
            kb.button(text=f'{user.username}', callback_data=f'barista_{user.id}')
        if status == "admin":
            kb.button(text=f'{user.username}', callback_data=f'admin_{user.id}')

    kb.adjust(3)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
    return kb.as_markup()
