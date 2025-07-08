import asyncio
import datetime

from aiogram import Bot
from aiogram.types import Message
from tortoise.exceptions import IntegrityError

from database.models_db import Horoscope
from database.zodiac_signs import zodiac_signs
from utils.ai_generator import Prompt, AiAssistent
from utils.config import SUPERADMIN
from utils.logging_config import horo_logger


async def start_generate_all_horoscopes(bot: Bot, date: datetime):
    """ Генерация всех гороскопов """
    for zodiac in zodiac_signs:
        await generate_horoscope(zodiac, int(date.month), int(date.year), bot)
        await bot.send_message(chat_id=SUPERADMIN, text=f'Генерирую гороскоп для знака {zodiac}')
        horo_logger.debug(f'SUPERADMIN: {SUPERADMIN}, Генерирую гороскоп для знака {zodiac}')
        await asyncio.sleep(60)


async def generate_horoscope(zodiac: str, month: int, year: int, bot: Bot):
    """
    Гороскоп на все дни месяца для одного знака.
    # Гороскоп имеет вид строки:
    # 1: Утро начнётся с эспрессо такой концентрации, что твоё расписание выстроится в идеальные столбцы
        # через ровно 47 секунд – не трогай планировщик, пока не допьешь!
    # 2: Крепость твоего американо сегодня = количество нервных раздражителей × 0.5 — ожидай поправку на летнее КПД и
        # найдешь ровно 5 кофейных зерен в неожиданном кармане (+бонусные 2.5 ступорных шага вперед).
    """
    system_prompt = Prompt.use_system_prompt(month)
    user_prompt = Prompt.use_user_prompt(zodiac, month, year)
    horo_logger.info(f'Начинаю генерацию гороскопа для {zodiac}')
    try:
        horoscope = await asyncio.to_thread(
            AiAssistent.get_completion,
            system_prompt,
            user_prompt
        )
        horo_logger.debug(f'получен гороскоп длинной : {len(horoscope)}')
        if not horoscope:
            raise ValueError("Пустой ответ от API")

        await asyncio.sleep(10)
        await horoscope_transformation_text(zodiac, horoscope, month, year, bot)
    except Exception as ex:
        horo_logger.exception(f'Ошибка получения гороскопа для {zodiac} - {ex}')


async def horoscope_transformation_text(zodiac: str, monthly_horoscope: str, month: int, year: int, bot: Bot):
    """ Преобразование полного гороскопа в отдельный ежедневный формат """
    horoscopes = {}
    horo_logger.info(f'Перехожу к тексту знака - {zodiac}')
    horo_logger.debug(f'Длинна гороскопа - {len(monthly_horoscope)}')
    for day_horoscope in monthly_horoscope.strip().split('\n'):
        horo_logger.debug(f'Строка гороскопа - {day_horoscope}')
        if ':' in day_horoscope:
            horo_logger.debug(f'строка: {day_horoscope}')
            date, daily_horoscope = day_horoscope.split(':', 1)
            # фильтруем даты из гороскопа
            date = date.split('.')[0]  # ''.join(filter(str.isdigit, day_part))
            horo_logger.debug(f'daily_horoscope для {zodiac} - {date} - {len(daily_horoscope)}')
            if date.isdigit():
                day = datetime.date(year, month, int(date))
                horo_logger.debug(f'day {zodiac} - {day} ')
                try:
                    horo_logger.info(f'Сохраняю гороскоп знака - {zodiac}')
                    await save_horoscope(zodiac, day, daily_horoscope.strip(), bot)

                    horoscopes[day] = daily_horoscope.strip()
                except ValueError:
                    horo_logger.warning(f'Что-то с текстом тексту знака - {zodiac}, {ValueError}')
                    continue


async def save_horoscope(zodiac: str, date: datetime, horoscope: str, bot: Bot):
    """ Сохранение гороскопа построчно (по датам) """
    try:
        await Horoscope.update_or_create(
            zodiac=zodiac,
            text=horoscope,
            date=date
        )
        horo_logger.info(f'Сохранил гороскоп знака - {zodiac}')

    except IntegrityError as e:
        # Обработка ошибки уникальности (дубликат записи)
        horo_logger.warning(f'Гороскоп для {zodiac} на {date} уже существует: {e}')
        await bot.send_message(chat_id=SUPERADMIN, text=f'Дата дублируется {zodiac}: {e}')

    except Exception as e:
        horo_logger.exception(f'Ошибка сохранения гороскопа {zodiac}: {e}')
        await bot.send_message(chat_id=SUPERADMIN, text=f'Не удалось сохранить гороскоп для {zodiac}: {e}')

