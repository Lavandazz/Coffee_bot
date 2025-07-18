from aiogram.types import TelegramObject
from redis.asyncio import Redis
from aiogram import BaseMiddleware
from typing import Callable, Dict, Any
from datetime import date

from database.models_db import User, Statistic
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


class StatisticMiddleware(BaseMiddleware):
    """ Мидлвар для сбора статисктики заходов в бот """

    def __init__(self, redis: Redis):
        self.redis = redis

    async def __call__(self,
                       handler: Callable,
                       event: TelegramObject,
                       data: Dict[str, Any]):

        user_id = event.from_user.id

        event_date = date.today()
        redis_key = f'user{user_id}:visit'

        bot_logger.debug(f'event_date: {event_date}\nredis_key: {redis_key}')

        try:
            # Проверяем, есть ли в базе ключ redis_key, то есть заходил ли пользователь
            already_seen = await self.redis.exists(redis_key)
            bot_logger.debug(f'already_seen: {already_seen}\n')
            if not already_seen:
                # Устанавливаем ключ с TTL до конца суток (24 часа)
                await self.redis.set(redis_key, str(event_date))
                await self.redis.expire(redis_key, 60 * 60 * 24)

            user = await User.get_or_none(telegram_id=event.from_user.id)  # 484385628
            stat, _ = await Statistic.get_or_create(day=event_date)
            stat.event += 1  # добавляем апдейт

            # Если пользователь ещё не зарегистрирован в БД — считаем как нового
            if not user:
                stat.new_user += 1
                # Добавим пользователя в таблицу (если хочешь)
                await User.create(telegram_id=user_id)

            await stat.save()

        except Exception as e:
            bot_logger.error(f"[StatsMiddleware] Ошибка статистики: {e}")

        # Передаём управление дальше в функции
        return await handler(event, data)
