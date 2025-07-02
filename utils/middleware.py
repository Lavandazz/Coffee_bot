from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Callable, Dict, Any

from aiohttp.typedefs import Middleware


class RoleMiddleware(BaseMiddleware):
    async def __call__(self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Any],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event['event_from_user'].id
