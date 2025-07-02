from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.horoscope import MockHoroscope
from database.models_db import Horoscope
from keyboards.back_keyboard import back_button
from keyboards.horoscope_keyboard import zodiac_kb
from states.menu_states import MenuState
from utils.shedulers.horo_scheduler import generate_horo


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
    horoscope = await Horoscope.get_or_none(zodiac=zodiac, date=call_date)
    if horoscope:
        await call.message.edit_text(f'Гороскоп на сегодня: {horoscope.text}',
                                     reply_markup=back_button())

    else:
        horoscope = await MockHoroscope.get_or_none(zodiac, call_date.month)
        await call.message.edit_text(f'Гороскоп на сегодня: {horoscope.get("text")}',
                                     reply_markup=back_button())


async def start_schedule_horo(call: CallbackQuery):
    await call.answer('Запускаю гороскоп')
    await generate_horo()
