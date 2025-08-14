from aiogram.types import TelegramObject
from redis.asyncio import Redis
from aiogram import BaseMiddleware
from typing import Callable, Dict, Any
from datetime import date, datetime

from tortoise.exceptions import DoesNotExist

from database.models_db import User, Statistic
from utils.logging_config import bot_logger


class RoleMiddleware(BaseMiddleware):
    """
    Middleware для обработки каждого события от пользователя.

    Функция выполняет:
    1. Определение пользователя по telegram_id.
    2. Если пользователь найден в базе — обновление времени его последней активности.
    3. Если пользователь не найден — создание нового пользователя с ролью "user".
    4. Запись в словарь data:
       - "role": роль пользователя.
       - "new_user": True, если пользователь зарегистрирован в этот момент, иначе False.

    После обработки передает управление следующему хендлеру в цепочке.
    """
    async def __call__(self, handler, event, data):
        try:
            user_id = event.from_user.id  # 7599073638
            user = await User.get_or_none(telegram_id=user_id)
            bot_logger.debug(f'Пользователь взаимодействует с ботом {user_id}')

            if user:
                # Если есть в базе — обновляем активность
                user.last_activity = datetime.now()
                await user.save()
                data["role"] = user.role
                data["new_user"] = False
            else:
                # Если нет в базе — создаем нового
                user = await User.create(
                    telegram_id=user_id,
                    first_name=event.from_user.first_name,
                    username=event.from_user.username,
                    role="user",
                    last_activity=datetime.now()
                )
                bot_logger.debug(f"Создан новый пользователь {user_id}")
                data["new_user"] = True
                data["role"] = "user"

        except Exception as e:
            bot_logger.exception(e)

        return await handler(event, data)


class StatisticMiddleware(BaseMiddleware):
    """
    Этот мидлвар записывает статистику посещений бота.
    Работа происходит через Redis базу. Создается пара Ключ - телеграм айди юзера: Значение - дата.
    Если пользователь уже заходил в бота в текущий день, то апдейт уже не учитывается.
    В бд постгрес сохраняется общее количество апдейтов за день.
    А так же, если был новый пользователь, то он тоже сохраняется в бд.
    """

    def __init__(self, redis: Redis):
        self.redis = redis

    async def __call__(self,
                       handler: Callable,
                       event: TelegramObject,
                       data: Dict[str, Any]):

        user_id = event.from_user.id
        event_date = date.today()

        redis_key = f'user{user_id}:visit'
        try:
            # Проверяем, есть ли в базе ключ redis_key, то есть заходил ли пользователь
            already_seen = await self.redis.exists(redis_key)
            # Создание в бд строки с датой
            stat, create_state = await Statistic.get_or_create(day=event_date)
            bot_logger.debug(f'stat создался при апдейте: {create_state}')
            if not already_seen:
                # Устанавливаем ключ с TTL до конца суток (24 часа)
                await self.redis.set(redis_key, "1", ex=60 * 60 * 24)
                # Сохраняем в бд
                await Statistic.filter(id=stat.id).update(event=stat.event + 1)

            if stat.event == 0:
                stat.event += 1  # добавляем апдейт
                bot_logger.debug(f'stat.event стал: {stat.event}')

                user = await User.get_or_none(telegram_id=event.from_user.id)

            # # Если пользователь ещё не зарегистрирован в БД — считаем как нового
            if data.get("new_user"):
                await Statistic.filter(id=stat.id).update(new_user=stat.new_user + 1)
            try:
                await stat.save()
            except Exception as e:
                bot_logger.error(f"[Ошибка сохранения в БД]: {e}")
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
