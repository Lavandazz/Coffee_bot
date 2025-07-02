from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat

from utils.config import get_admin_id
from utils.if_admin import is_admin


async def set_commands(bot: Bot, user_id: int = None):
    """ Создание кнопок """
    commands = [
        BotCommand(command='start',
                   description='Запуск бота'),
        BotCommand(command='help',
                   description='Помощь')
    ]

    admin_commands = commands + [
        BotCommand(command="admin",
                   description="Админ-панель")
    ]


    # Устанавливаем команды по умолчанию
    await bot.set_my_commands(commands, BotCommandScopeDefault())

    admin = await is_admin(user_id)
    # admins = get_admin_id()
    # Дополнительно устанавливаем для админов
    if admin:
    # for admin_id in admins:
        await bot.set_my_commands(
            commands=admin_commands,
            scope=BotCommandScopeChat(chat_id=admin)
        )
