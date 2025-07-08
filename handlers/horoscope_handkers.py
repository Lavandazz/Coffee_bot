from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.horoscope import MockHoroscope
from database.models_db import Horoscope
from keyboards.back_keyboard import back_button
from keyboards.horoscope_keyboard import zodiac_kb
from states.menu_states import MenuState
from utils.logging_config import bot_logger
from utils.shedulers.horo_scheduler import generate_call_horo


async def show_horoscope(call: CallbackQuery, state: FSMContext):
    """ Отображение знаков зодиака в клавиатуре """
    await state.set_state(MenuState.horoscope_menu)
    await call.message.edit_text('Выбери свой знак', reply_markup=zodiac_kb())


async def send_horoscope(call: CallbackQuery, state: FSMContext):
    """ Обработка кнопки знака зодиака """
    call_date = call.message.date.date()
    zodiac = call.data.replace('zodiac_', '')
    await state.set_state(MenuState.zodiac_menu)
    # получаем гороскоп их псевдобазы
    try:
        horoscope = await Horoscope.get_or_none(zodiac=zodiac, date=call_date)

        if horoscope:
            if call_date == horoscope.date:
                await call.message.edit_text(f'Гороскоп на сегодня:\n{horoscope.text}',
                                             reply_markup=back_button())
            else:
                horoscope = await MockHoroscope.get_or_none(zodiac)
                await call.message.edit_text(f'Гороскоп на сегодня:\n{horoscope.get("text")}',
                                             reply_markup=back_button())
                bot_logger.warning(f'Дата гороскопа не совпадает {zodiac}, {call_date}')
        else:
            horoscope = await MockHoroscope.get_or_none(zodiac)
            await call.message.edit_text(f'Гороскоп на сегодня:\n{horoscope.get("text")}',
                                         reply_markup=back_button())
            bot_logger.warning(f'Гороскопа для {zodiac} нет в базе {call_date}. Использована мокбаза')
    except Exception as e:
        await call.message.answer("Произошла ошибка, попробуйте позже")
        bot_logger.info(f'Ощибка в отправке гороскопа для {zodiac}, error: {e}')


async def start_schedule_horo(call: CallbackQuery):
    """ Ручной запуск парсинга гороскопа """
    await call.answer('Запускаю гороскоп')
    await generate_call_horo(call)
