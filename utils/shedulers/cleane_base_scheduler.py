from utils.config import admin_id

from aiogram import Bot
from aiogram.types import CallbackQuery
from pytz import timezone
from datetime import datetime, date
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.models_db import Horoscope
from utils.logging_config import scheduler_logger


def get_first_day_next_month() -> date:
    """Вычисляем первый день следующего месяца."""
    today = datetime.now().date()
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)
    return next_month


async def horo_to_clean(bot: Bot):
    """ Получение данных для удаления"""
    current_date = datetime.now().date()
    # находим все даты меньше вчерашней и удаляем их
    old_horoscopes = await Horoscope.filter(date__lt=current_date).count()
    await bot.send_message(chat_id=admin_id, text=f'удалено {old_horoscopes} трок гороскопа')
    # await call.message.answer(text=f'удалено {old_horoscopes} трок гороскопа')


async def scheduler_clean_horoscope(bot: Bot):
    """ Запуск шедулера """
    horo_timezone = timezone('Europe/Moscow')
    scheduler = AsyncIOScheduler()
    # scheduler.add_job(horo_to_clean, "cron", hour=13, minute=53, timezone=horo_timezone, args=[bot])
    scheduler.add_job(horo_to_clean, "date",
                      run_date=datetime(2025, 7, 2, 14, 37),
                      timezone=horo_timezone,
                      args=[bot])
    scheduler.start()
    scheduler_logger.info(f'Шедулер очистки дат запущен в {datetime.now()}')
