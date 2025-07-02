from aiogram import Bot
from aiogram.types import Message
from datetime import timezone

from database.models_db import User
from keyboards.menu_keyboard import inline_menu_kb
from utils.ai_generator import generate_day_or_night
from utils.logging_config import bot_logger


async def on_start(bot: Bot):
    """ Отправка сообщения о старте админу """
    await bot.send_message(484385628, text='Я запустил CoffeeBot')


async def get_start(message: Message, bot: Bot):
    """ Старт приложения """
    time_message = message.date
    # Преобразуем часовой пояс (+3 часа для Москвы)
    local_time = time_message.replace(tzinfo=timezone.utc).astimezone(tz=None)  # Автоматически определит локальный пояс
    user_id = await User.filter(telegram_id=message.from_user.id).exists()  # проверка айди в базе
    if not user_id:
        await User.create(
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            telegram_id=message.from_user.id,
            is_admin=False)
        bot_logger.info(f'Зарегистрирован новый пользователь {message.from_user.id}')
    await bot.send_message(message.from_user.id,
                           f"{generate_day_or_night(local_time.hour)}",
                           reply_markup=inline_menu_kb())