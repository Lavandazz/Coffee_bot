import asyncio
import datetime
from database.models_db import Horoscope
from database.zodiac_signs import zodiac_signs
from utils.ai_generator import Prompt, AiAssistent
from utils.logging_config import horo_logger


async def start_generate_all_horoscopes(date: datetime):
    """ Генерация всех гороскопов """
    for zodiac in zodiac_signs:
        await generate_horoscope(zodiac, int(date.month), int(date.year))
        await asyncio.sleep(60)


async def generate_horoscope(zodiac: str, month: int, year: int):
    """ Гороскоп на все дни месяца для одного знака """
    """ 
    # Получаем строку со всеми датами за месяц.
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

        print('сплю 10 сек')
        print(f'Получен horoscope для знака {zodiac}: {horoscope[:70]}')
        await asyncio.sleep(10)
        await horoscope_transformation_text(zodiac, horoscope, month, year)
    except Exception as ex:
        horo_logger.exception(f'Ошибка получения гороскопа для {zodiac} - {ex}')


async def horoscope_transformation_text(zodiac: str, monthly_horoscope: str, month: int, year: int):
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
                    await save_horoscope(zodiac, day, daily_horoscope.strip())

                    horoscopes[day] = daily_horoscope.strip()
                except ValueError:
                    horo_logger.warning(f'Что-то с текстом тексту знака - {zodiac}, {ValueError}')
                    continue


async def save_horoscope(zodiac: str, date: datetime, horoscope: str):
    """ Сохранение гороскопа построчно (по датам) """
    try:
        await Horoscope.create(
            zodiac=zodiac,
            text=horoscope,
            date=date
        )
        horo_logger.info(f'Сохранил гороскоп знака - {zodiac}')

    except Exception as e:
        print(f'не удалось сохранить гороскоп для {zodiac}', e)
