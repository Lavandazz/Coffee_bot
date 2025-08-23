from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.get_user import get_role_user
from utils.logging_config import bot_logger


async def inline_menu_kb(user_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(text='Поделиться фото', callback_data='share_photo')
    kb.button(text='Поделиться пожеланием', callback_data='share_wish')
    kb.button(text='Кофейный гороскоп', callback_data='horoscope')
    kb.button(text=f'Мероприятия / Игры', callback_data='games_all')
    kb.adjust(2)

    role = await get_role_user(user_id)  # получаем роль юзера
    bot_logger.debug(f'Передаю inline_menu_kb. Роль юзера: {role}')
    if role == 'admin' or role == 'barista':
        kb.row(InlineKeyboardButton(text='Админ-панель', callback_data='admin_panel'))

    return kb.as_markup()


def start_for_channel():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Подписаться на канал", url="https://t.me/coffee_v_zernah")]
        ]
    )
    return kb.as_markup()