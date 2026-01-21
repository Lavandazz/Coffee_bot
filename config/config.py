import os

from aiogram.fsm.storage.redis import RedisStorage

from redis.asyncio import Redis
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import Bot, Dispatcher


# Импортируем путь к env файлу с загруженным окружением
from .settings_env import env_path


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

storage = RedisStorage(redis=redis_client)

# Объекты бота
bot = Bot(
    token=token,
    session=AiohttpSession(),
    default=DefaultBotProperties(parse_mode="HTML")
)
# dp = Dispatcher(storage=storage)
dp = Dispatcher()
