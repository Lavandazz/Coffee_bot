from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from datetime import timezone
from aiogram.types import ChatMemberLeft
from tortoise.exceptions import IntegrityError

from database.models_db import User
from keyboards.menu_keyboard import inline_menu_kb, start_for_channel
from utils.ai_generator import generate_day_or_night
from utils.config import SUPERADMIN, CHANNEL, CHANNEL_ID
from utils.logging_config import bot_logger


async def on_start(bot: Bot):
    """ Отправка сообщения о старте супер-админу """
    await bot.send_message(chat_id=SUPERADMIN, text='Я запустил CoffeeBot')


async def seed_admin():
    """
    При старте приложения, будет создан супер-админ
    """
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
    """
    Старт приложения.
    Если пользователя еще нет в базе, то он будет зарегистрирован.
    При регистрации нового пользователя отправляется сообщение супер-админу. (Можно сделать рассылку админам)
    """
    time_message = message.date
    # Преобразуем часовой пояс (+3 часа для Москвы)
    local_time = time_message.replace(tzinfo=timezone.utc).astimezone(tz=None)  # определяет локальный пояс
    try:
        create_u = await create_user(message.from_user.username, message.from_user.first_name,
                                     message.from_user.id)
        if create_u:
            await bot.send_message(chat_id=SUPERADMIN, text=f'Зарегистрирован новый пользователь {message.from_user.id}')

        await bot.send_message(message.from_user.id,
                               f"{generate_day_or_night(local_time.hour)}",
                               reply_markup=await inline_menu_kb(message.from_user.id))
        await start_handler(message.from_user.id, bot)
    except Exception as e:
        bot_logger.exception(f'Ошибка при создании админа {e}')


async def create_user(username: str, first_name: str, telegram_id: int):
    """ Регистрация нового пользователя """
    try:
        user_id = await User.filter(telegram_id=telegram_id).exists()  # проверка айди в базе
        if not user_id:
            await User.create(
                username=username,
                first_name=first_name,
                telegram_id=telegram_id,
                is_admin=False)
            bot_logger.info(f'Зарегистрирован новый пользователь {telegram_id}')
            return True

    except Exception as e:
        bot_logger.error(f'Ошибка регистрации нового пользователя, {e}')


async def is_user_in_channel(user_id: int, channel_id: int, bot: Bot) -> bool:
    """ Проверка, есть ли пользователь в чате """
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        # сравниваем со строкой: 	The member's status in the chat, always “left”
        return member.status != 'left'

    # если ошибка, то пользователя в чате нет
    except TelegramBadRequest as e:
        bot_logger.warning(f'Пользователя {user_id} нет в канале')
        return False


async def start_handler(user_id, bot: Bot):
    """
    Если пользователя нет в канале кофейни, то ему будет отправлено уведомление об этом с приглашением
    вступить в канал.
    """
    try:
        invite_link = await bot.create_chat_invite_link(chat_id=CHANNEL_ID, name="Наш канал ☕")
        if not await is_user_in_channel(user_id, CHANNEL_ID, bot):
            await bot.send_message(
                chat_id=user_id,
                text=f"☕ Добро пожаловать! Подпишись на наш канал: {invite_link.invite_link}"
            )
            bot_logger.info(f'Отправил ссылку на канал: {invite_link.invite_link}')
    except Exception as e:
        bot_logger.exception(f'Не получилось отправить ссылку {e}')


