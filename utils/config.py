import os
from redis.asyncio import Redis
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from .settings_env import env_file


# Переменные окружения
token = os.getenv("BOT_TOKEN")
admin_id = os.getenv("ADMIN")
API_KEY = os.getenv("OPENROUTER_API_KEY")
SUPERADMIN = int(admin_id.replace(',', ''))
CHANNEL = os.getenv("CHANNEL_NAME")
CHANNEL_ID = os.getenv("CHANNEL_ID")


redis_client = Redis(host=os.getenv("REDIS_HOST"),
                     port=int(os.getenv("REDIS_PORT")),
                     db=int(os.getenv("REDIS_DB")),
                     password=os.getenv("REDIS_PASSWORD"),
                     decode_responses=True)  # чтобы строки были не в байтах

# Объекты бота
bot = Bot(
    token=token,
    session=AiohttpSession(),
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()


def get_admin_id() -> list[int]:
    """ Преобразование строки админов в инт """
    return [int(x.strip()) for x in admin_id.split(",") if x.strip().isdigit()]


