from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_review_keyboard(review_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Одобрить", callback_data=f"approve_{review_id}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_{review_id}")
        ]
    ])


async def get_back(back_state):
    """ Кнопка Назад """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_admin_menu")]
    ])
