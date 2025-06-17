from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from handlers.register import start_register


class CheckUserMiddleware(BaseMiddleware):
    def __init__(self, db):
        super().__init__()
        self.db = db  # Передаем экземпляр базы данных

    async def __call__(self, handler, update, data):
        user_id = None
        """ Определяем пользователя по ID """
        if isinstance(update, Message):
            user_id = update.from_user.id
        elif isinstance(update, CallbackQuery):
            user_id = update.from_user.id
        """ Проверяем регистрацию """
        if user_id:
            user = await self.db.select_user(user_id)
            if not user:
                bot = data.get('bot')
                state = data.get('state')

                if isinstance(update, Message):
                    await start_register(update, state, bot)
                elif isinstance(update, CallbackQuery):
                    await start_register(update.message, state, bot)
                return
        return await handler(update, data)
