from aiogram import Bot
from aiogram.types import Message
from datetime import timezone

from tortoise.exceptions import IntegrityError

from database.models_db import User
from keyboards.menu_keyboard import inline_menu_kb
from utils.ai_generator import generate_day_or_night
from utils.config import admin_id, SUPERADMIN
from utils.logging_config import bot_logger


async def on_start(bot: Bot):
    """ Отправка сообщения о старте админу """
    await bot.send_message(chat_id=SUPERADMIN, text='Я запустил CoffeeBot')


async def seed_admin():
    """ Регистрация админа """
    bot_logger.info('Проверка: seed_admin вызвана')
    try:
        admin = await User.filter(role='admin').exists()
        if not admin:
            await User.create(
                username="Админ",
                telegram_id=SUPERADMIN,
                first_name="Админ",
                role="admin"
            )
            bot_logger.info('Администратор зарегистрирован')

    except IntegrityError as e:
        bot_logger.info("Админ уже существует, пропускаем создание")

    except Exception as e:
        bot_logger.exception(f'Ошибка при создании админа {e}')


async def get_start(message: Message, bot: Bot):
    """ Старт приложения """
    time_message = message.date
    # Преобразуем часовой пояс (+3 часа для Москвы)
    local_time = time_message.replace(tzinfo=timezone.utc).astimezone(tz=None)  # определяет локальный пояс
    try:
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
                               reply_markup=await inline_menu_kb(message.from_user.id))
    except Exception as e:
        bot_logger.exception(f'Ошибка при создании админа {e}')
