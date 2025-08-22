from typing import List

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models_db import Game


def games_kb():
    """
    Меню игр
    :return:
    """
    kb = InlineKeyboardBuilder()
    kb.button(text='Предстоящие игры', callback_data='show_upcoming_games')
    kb.button(text='Прошедшие игры', callback_data='show_passed_games')
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
    return kb.as_markup()


async def show_games_kb(games: List[Game]):
    """
    Отображение клавиатуры с играми
    :param games: Передаем список объектов игр
    :return: kb
    """
    kb = InlineKeyboardBuilder()
    if games:
        for game in games:
            kb.button(text=game.title, callback_data=f'game_')
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
    return kb.as_markup()

