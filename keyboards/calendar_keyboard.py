from datetime import date
from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def calendar_kb(days: List[date], month: str) -> InlineKeyboardMarkup:
    """
    Создаёт inline-клавиатуру календаря.

    В верхней строке находятся кнопки навигации по месяцам:
    [⬅️] [Название месяца] [➡️]

    Далее располагаются кнопки с днями месяца (по 7 в строке).
    Внизу отдельной строкой добавляется кнопка "❌ Выход".

    :param days: Список объектов datetime.date, представляющих дни месяца.
                 Порядок элементов определяет порядок отображения кнопок.
    :param month: Название месяца для отображения в шапке (например, "Август 2025").
    :return: Объект InlineKeyboardMarkup с разметкой календаря.
    """
    # Билдер для дней — добавляем только дни и выравниваем в ряды по 7
    days_builder = InlineKeyboardBuilder()
    for d in days:
        days_builder.button(
            text=d.strftime('%d'),
            callback_data=f"day_{d.strftime('%d.%m.%Y')}"
        )
    days_builder.adjust(7)  # разбиваем ряды по 7

    # Финальный билдер — сначала шапка (навигация), затем прикрепляем дни, затем выход
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text='⬅️', callback_data='prev_month'),
        InlineKeyboardButton(text=month, callback_data='month'),
        InlineKeyboardButton(text='➡️', callback_data='next_month'),
    )
    kb.attach(days_builder)  # вставляем уже отрегулированные ряды с днями
    kb.row(InlineKeyboardButton(text='❌ Выход', callback_data='back'))

    return kb.as_markup()
