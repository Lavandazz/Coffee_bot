from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.if_admin import get_role_user


async def inline_menu_kb(user_id):
    kb = InlineKeyboardBuilder()
    kb.button(text='Поделиться фото', callback_data='share_photo')
    kb.button(text='Поделиться пожеланием', callback_data='share_wish')
    kb.button(text='Кофейный гороскоп', callback_data='horoscope')
    kb.button(text='Акции', callback_data='stocks')
    kb.adjust(2)

    role = await get_role_user(user_id)
    if role == 'admin' or role == 'barista':
        kb.row(InlineKeyboardButton(text='Админ-панель', callback_data='admin_panel'))

    return kb.as_markup()
