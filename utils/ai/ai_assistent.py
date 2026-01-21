from openai import OpenAI, RateLimitError

from config.config import API_KEY
from utils.ai.models_ai import MISTRAL_MODEL

from config.logging_config import help_ai_logger


class AiAssistent:
    _client = None

    @classmethod
    def client(cls):
        if cls._client is None:
            cls._client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=API_KEY,
            )
        return cls._client

    @classmethod
    def get_completion(cls, system_prompt: str, user_prompt: str) -> str:
        """ Получаем готовый текст кофейного предсказания """
        try:
            help_ai_logger.info('Генерирую ответ')
            completion = cls.client().chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://t.me/fragrant_coffee_bot",
                    "X-Title": "CoffeeBot"
                },
                extra_body={},
                model="deepseek/deepseek-r1-0528:free",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
            )
            help_ai_logger.info('Получил ответ')
            help_ai_logger.info('completion', completion.choices[0].message.content)
            return completion.choices[0].message.content

        except Exception as ex:
            help_ai_logger.exception(f"Ошибка в AiAssistent: {ex}")
