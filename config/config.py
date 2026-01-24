from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import Bot, Dispatcher

from config.settings_env import settings


token = settings.BOT_TOKEN
admin_id = settings.ADMIN
API_KEY = settings.OPENROUTER_API_KEY
SUPERADMIN = int(admin_id.replace(',', ''))
CHANNEL = settings.CHANNEL_NAME
CHANNEL_ID = settings.CHANNEL_ID


# Объекты бота
bot = Bot(
    token=token,
    session=AiohttpSession(),
    default=DefaultBotProperties(parse_mode="HTML")
)
# dp = Dispatcher(storage=storage)
dp = Dispatcher()
