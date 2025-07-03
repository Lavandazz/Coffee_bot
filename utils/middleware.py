from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Callable, Dict, Any

from aiohttp.typedefs import Middleware

from database.models_db import User


class RoleMiddleware(BaseMiddleware):
    async def __call__(self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Any],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        user = await User.get(telegram_id=user_id)
        data["role"] = user.role if user else "user"
        return await handler(event, data)
