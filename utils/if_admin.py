from database.models_db import User
from utils.logging_config import bot_logger


async def is_admin(user_id):
    """ Проверка администратора """
    admin = await User.filter(telegram_id=user_id, role='admin').exists()
    bot_logger.info(f'admin = {admin}')
    return admin

