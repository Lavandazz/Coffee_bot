import asyncio

from utils.ai.ai_assistent import AiAssistent
from config.logging_config import help_ai_logger
from utils.ai.prompts import BaristaPrompt


async def generate_ai_greeting():
    # Тут потом можно будет подключить OpenAI, Gemini, Mistral и т.д.
    # return "Доброе утро! Ваш кофе готов ☕"
    system_prompt = BaristaPrompt.use_system_prompt()
    user_prompt = BaristaPrompt.use_user_prompt()
    help_ai_logger.debug("Генерирую фразу для бариста")
    try:
        phrase = await asyncio.to_thread(
            AiAssistent.get_completion,
            system_prompt,
            user_prompt
        )
        help_ai_logger.info("Ответ для бариста получен")
        return phrase

    except Exception as ex:
        help_ai_logger.exception(f'Ошибка получения фразы для бариста - {ex}')
