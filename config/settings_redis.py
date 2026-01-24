from aiogram.fsm.storage.redis import RedisStorage

from redis.asyncio import Redis

from config.settings_env import settings


redis_client = Redis(host=settings.REDIS_HOST,
                     port=settings.REDIS_PORT,
                     db=settings.REDIS_DB,
                     password=settings.REDIS_PASSWORD,
                     decode_responses=True)  # чтобы строки были не в байтах

storage = RedisStorage(redis=redis_client)