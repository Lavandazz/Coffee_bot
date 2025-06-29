import logging
import datetime
# from datetime import datetime, timedelta

from openai import OpenAI
from tortoise.transactions import in_transaction

from .config import API_KEY
from database.models_db import Horoscope
from database.zodiac_signs import zodiac_signs
from utils.ai_generator import Prompt, AiAssistent

main_logger = logging.getLogger('main')

MODEL = "mistralai/mistral-small-24b-instruct-2501:free"


async def generate_coffee_horoscope(date: datetime):
    """ Генерация гороскопа """
    system_prompt = Prompt.use_system_prompt(int(date.month))
    for zodiac in zodiac_signs:
        user_prompt = Prompt.use_user_prompt(zodiac, int(date.month), int(date.year))
        horoscope = AiAssistent.get_completion(system_prompt, user_prompt)

        await parse_response(zodiac, horoscope, date)


async def parse_response(zodiac: str, zodiac_horoscope: str, date: datetime):
    """ Преобразование строк для последующего сохранения """
    horoscope_lines = zodiac_horoscope.strip().split('\n')
    parsed = {}

    for day_horoscope in horoscope_lines:
        if ':' in day_horoscope:
            day_date_str, horoscope_text = day_horoscope.split(':', 1)
            # фильтруем даты
            day_date_str = day_date_str.split('.')[0]  # ''.join(filter(str.isdigit, day_part))
            if day_date_str.isdigit():
                try:
                    day_horo_date = datetime.date(date.year, date.month, int(day_date_str))
                    parsed[day_horo_date] = horoscope_text.strip()
                except ValueError:
                    continue
    print(f'parsed: {parsed}')
    await save_horoscope(zodiac, parsed)
    # return parsed


async def save_horoscope(zodiac: str, horoscope: dict):
    """ Сохранение в БД """
    try:
        async with in_transaction():
            for date, text in horoscope.items():
                await Horoscope.update_or_create(
                    defaults={"text": text},
                    zodiac=zodiac,
                    date=date
                )

    except Exception as e:
        main_logger.error(f'Ошибка сохранения гороскопа: {e} ')


# async def generate_and_save(zodiac: str, year: int, month: int):
#     parsed = await generate_coffee_horoscope(zodiac, year, month)
#     await save_horoscope(zodiac, parsed)


# async def generate_all_horoscopes(year: int, month: int):
#     """ Генерация для всех зодиаков (для шедулера) """
#     for zodiac in ZODIAC_SIGNS:
#         try:
#             await generate_and_save(zodiac, year, month)
#         except Exception as e:
#             main_logger.error(f"Ошибка при генерации для {zodiac}: {e}")