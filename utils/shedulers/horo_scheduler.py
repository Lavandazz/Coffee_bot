from aiogram import Bot
from aiogram.client import bot
from aiogram.types import CallbackQuery
from pytz import timezone
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.generator_horoscope import start_generate_all_horoscopes
from utils.logging_config import scheduler_logger


async def generate_call_horo(call: CallbackQuery):
    """ Ручной запуск генерации гороскопа """
    now_date = datetime.now().date()
    bot = call.bot
    await start_generate_all_horoscopes(bot, now_date)


async def generate_horo(bot: Bot):
    """ Вызов генерации гороскопа для шедулера"""
    now_date = datetime.now().date()
    await start_generate_all_horoscopes(bot, now_date)


async def scheduler_horoscope():
    """ Запуск шедулера """
    horo_timezone = timezone('Europe/Moscow')

    scheduler = AsyncIOScheduler()
    scheduler.add_job(generate_horo, "cron", hour=15, minute=22, timezone=horo_timezone,
                      args=[bot])
    scheduler.start()
    # scheduler_logger.info(f'Гороскопный шедулер запущен в {datetime.now()}')