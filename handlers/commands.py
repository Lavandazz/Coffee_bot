from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat

from utils.config import get_admin_id


async def set_commands(bot: Bot):
    """ Создание кнопок """
    commands = [
        BotCommand(command='start',
                   description='Запуск бота'),
        BotCommand(command='help',
                   description='Помощь')
    ]

    admin_commands = commands + [
        BotCommand(command="moderate",
                   description="Отзывы"),
        BotCommand(command="admin",
                   description="Админ-панель")
    ]


    # Устанавливаем команды по умолчанию
    await bot.set_my_commands(commands, BotCommandScopeDefault())

    admins = get_admin_id()
    # Дополнительно устанавливаем для админов
    for admin_id in admins:
        await bot.set_my_commands(
            commands=admin_commands,
            scope=BotCommandScopeChat(chat_id=admin_id)
        )
