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
    def get_completion(cls, system_prompt: str, user_prompt: str, max_retries: int = 5) -> str:
        """ Получаем готовый текст кофейного предсказания """
        # подсчитываем число неудачных попыток из-за RateLimitError
        retry_count = 0

        while retry_count <= max_retries:
            try:
                help_ai_logger.info(f"Генерирую ответ (попытка {retry_count + 1})")
                completion = cls.client().chat.completions.create(
                    extra_headers={
                        "HTTP-Referer": "https://t.me/fragrant_coffee_bot",
                        "X-Title": "CoffeeBot"
                    },
                    model=MISTRAL_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ]
                )
                help_ai_logger.info("Получил ответ от генератора")
                return completion.choices[0].message.content

            except RateLimitError as e:
                retry_count += 1
                if retry_count > max_retries:
                    help_ai_logger.error(f"Превышено максимальное количество попыток генерации({max_retries}): %s", e)
                    raise

            except Exception as ex:
                help_ai_logger.exception(f"Ошибка в AiAssistent: {ex}")
