from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def hour_kb():
    """
    Клавиатура отображает время как кнопки с шагом в полчаса.
    :return: kb
    """
    kb = InlineKeyboardBuilder()
    for hour in range(11, 21):
        for minute in range(0, 60, 30):
            kb.button(text=f"{hour:02d}:{minute:02d}", callback_data=f"time_{hour:02d}:{minute:02d}")
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='❌ Отмена', callback_data='back'))
    return kb.as_markup()
