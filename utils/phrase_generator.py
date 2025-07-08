import asyncio

from utils.ai_generator import BaristaPrompt, AiAssistent
from utils.logging_config import help_ai_logger


async def generate_phrase():
    system_prompt = BaristaPrompt.use_system_prompt()
    user_prompt = BaristaPrompt.use_user_prompt()
    help_ai_logger.info('Генерирую фразу для бариста')
    try:
        phrase = await asyncio.to_thread(
            AiAssistent.get_completion,
            system_prompt,
            user_prompt
        )
        print('Получен ответ от ИИ', phrase)
        return phrase
    except Exception as ex:
        help_ai_logger.exception(f'Ошибка получения фразы для бариста - {ex}')
