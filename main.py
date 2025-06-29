import asyncio

from handlers.commands import set_commands
from handlers.dispatcher import setup_dispatcher
from utils.config import dp, bot
from database.create_db import init_db, close_db
from utils.schedulers import scheduler_horoscope

from utils.logging_config import bot_logger


async def start_bot():
    """ Запуск бота, при неудаче бот закроется """
    await set_commands(bot)
    # Регистрация хэндлеров
    setup_dispatcher(dp)
    asyncio.create_task(scheduler_horoscope())
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        bot_logger.warning('Бот закрыт')
        await bot.close()


async def main():
    # Подключаем БД ОДИН РАЗ
    await init_db()
    await start_bot()
    await close_db()  # Закроем БД после завершения всех задач


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        bot_logger.warning('Помощник завершены')
