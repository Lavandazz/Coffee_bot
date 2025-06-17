import asyncio
import datetime
import logging

from handlers.commands import set_commands
from handlers.dispatcher import setup_dispatcher
from utils.config import token, dp, bot
from database.create_db import init_db, close_db
from utils.logging_config import setup_logging

logging.basicConfig(level=logging.INFO)
main_logger = logging.getLogger('main')

setup_logging()


async def start_bot():
    """ Запуск бота, при неудаче бот закроется """
    await set_commands(bot)
    # Регистрация хэндлеров
    setup_dispatcher(dp)
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        main_logger.warning('Бот закрыт')
        await bot.close()


async def main():
    # Подключаем БД ОДИН РАЗ
    await init_db()
    await start_bot()
    await close_db()  # Закроем БД после завершения всех задач


if __name__ == '__main__':
    main_logger = logging.getLogger('main')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        main_logger.warning('Помощник завершены')
