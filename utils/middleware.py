import asyncio

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Callable, Dict, Any

from aiohttp.typedefs import Middleware

from database.models_db import User
from utils.logging_config import bot_logger


class RoleMiddleware(BaseMiddleware):

    async def __call__(self, handler, event, data):
        try:
            user_id = event.from_user.id
            user = await User.get(telegram_id=user_id)
            data["role"] = user.role if user else "user"
        except Exception as e:
            bot_logger.error(f"DB error in middleware: {e}")
            data["role"] = "user"
        return await handler(event, data)

