from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat

from utils.config import get_admin_id
from utils.if_admin import is_admin, get_role_user
from utils.logging_config import bot_logger


async def set_commands(bot: Bot, user_id: int = None):
    """ Создание кнопок """
    commands = [
        BotCommand(command='start',
                   description='Запуск бота')
        # BotCommand(command='help',
        #            description='Помощь')
    ]
    barista_commands = commands + [
        BotCommand(command="barista",
                   description="Панель-бариста")
    ]
    admin_commands = (commands + barista_commands +
                      [
                          BotCommand(command="admin",
                                     description="Админ-панель")
                      ])

    # Устанавливаем команды по умолчанию
    await bot.set_my_commands(commands, BotCommandScopeDefault())

    # admin = await is_admin(user_id)
    # Дополнительно устанавливаем для админов
    # role = await get_role_user(user_id)
    # if role == 'admin':
    #     await bot.set_my_commands(
    #             commands=admin_commands,
    #             scope=BotCommandScopeChat(chat_id=user_id)
    #         )
    #
    # if role == 'barista':
    #     await bot.set_my_commands(
    #         commands=barista_commands,
    #         scope=BotCommandScopeChat(chat_id=user_id)
    #     )
    bot_logger.info('Установил команды')
