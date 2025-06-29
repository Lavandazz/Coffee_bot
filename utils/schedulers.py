import asyncio
import os
from pytz import timezone
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.generator_horoscope import start_generate_all_horoscopes
from utils.logging_config import scheduler_logger


async def generate_horo():
    """ Вызов генерации гороскопа для шедулера"""
    now_date = datetime.now().date()
    await start_generate_all_horoscopes(now_date)


async def scheduler_horoscope():
    """ Запуск шедулера """
    horo_timezone = timezone('Europe/Moscow')

    scheduler = AsyncIOScheduler()
    scheduler.add_job(generate_horo, "cron", hour=15, minute=22, timezone=horo_timezone)
    scheduler.start()
    # scheduler_logger.info(f'Гороскопный шедулер запущен в {datetime.now()}')