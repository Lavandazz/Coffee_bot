from tortoise.exceptions import DoesNotExist

from database.models_db import User
from utils.logging_config import bot_logger


async def is_admin(user_id) -> bool:
    """ Проверка администратора """
    # admin = await User.filter(telegram_id=user_id, role='admin').exists()
    # # barista = await User.filter(telegram_id=user_id, role='barista').exists()
    # if admin:
    #     bot_logger.info(f'Админ {admin}')
    #     return admin
    try:
        user = await User.get(telegram_id=user_id)
        return user.role in ['admin', 'barista']
    except DoesNotExist:
        return False


async def get_users_from_db(user_role) -> list[dict]:
    """ Список словарей юзеров по ролям """
    users = await User.filter(role=user_role).values('id', 'username', 'telegram_id', 'role')
    return users


async def get_role_user(user_id) -> str | None:
    try:
        user = await User.get(telegram_id=user_id)  # telegram_id=484385628
        if user:
            return user.role
    except DoesNotExist:
            return None
