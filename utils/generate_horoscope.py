import httpx
import asyncio
import datetime
from config import API_KEY


async def generate_coffee_horoscope(zodiac: str) -> str:
    """ Запрос к ИИ для генерации гороскопа """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openchat/openchat-3.5",  # бесплатная модель
        "messages": [
            {
                "role": "system",
                "content": (
                    "Ты добрый мистический астролог и гадатель на кофейной гуще. "
                    "Говори загадочным, образным языком, используй метафоры. "
                    "Твой стиль — будто древний мудрец в тумане."
                )
            },
            {
                "role": "user",
                "content": f"Составь кофейный гороскоп на месяц для знака зодиака: {zodiac}."
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        print("result в гороскопе:", result)
        return result["choices"][0]["message"]["content"]



