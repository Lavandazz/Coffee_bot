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
            user_id = event.from_user.id  # 7599073638
            bot_logger.debug(f'Новый пользователь {event.from_user.id}')
            user = await User.get(telegram_id=user_id)
            bot_logger.debug(f'Узер {user.id, user.first_name, user.role}')

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

        # bot_logger.debug(f'event_date: {event_date}\nredis_key: {redis_key}')

        try:
            # Проверяем, есть ли в базе ключ redis_key, то есть заходил ли пользователь
            already_seen = await self.redis.exists(redis_key)
            # bot_logger.debug(f'~~~~ already_seen ~~~~ {already_seen}')

            stat, _ = await Statistic.get_or_create(day=event_date)
            # bot_logger.debug(f'Дата {stat.day} апдейтов {stat.event} ')

            if not already_seen:
                # Устанавливаем ключ с TTL до конца суток (24 часа)
                await self.redis.set(redis_key, "1", ex=60 * 60 * 24)

                await Statistic.filter(id=stat.id).update(event=stat.event + 1)
                # bot_logger.debug(f'stat.event в if not already_seen: {stat.event}')

            if stat.event == 0:
                stat.event += 1  # добавляем апдейт
                # bot_logger.debug(f'stat.event стал: {stat.event}')

                user = await User.get_or_none(telegram_id=event.from_user.id)  # 484385628
            # Если пользователь ещё не зарегистрирован в БД — считаем как нового
                if not user:
                    await Statistic.filter(id=stat.id).update(new_user=stat.new_user + 1)

            try:
                await stat.save()
            except Exception as e:
                print(f"[Ошибка сохранения в БД]: {e}")
            #
            # keys = await self.redis.keys("user*")
            # print(len(keys))
            # for key in keys:
            #     value = await self.redis.get(key)
            #     print(f"Все юзеры {key}: {value}")

        except Exception as e:
            bot_logger.error(f"[StatisticMiddleware] Ошибка статистики: {e}")

        # Передаём управление дальше в функции
        return await handler(event, data)
