from datetime import date
from typing import List

from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.models_db import Statistic
from keyboards.admin_keyboards import admin_stat_kb
from keyboards.back_keyboard import back_button
from keyboards.calendar_keyboard import calendar_kb
from states.menu_states import StatsState, AdminMenuState
from utils.custom_calendar import MyCalendar
from utils.date_formats import from_str_to_date_day
from utils.get_user import admin_only
from utils.logging_config import bot_logger


@admin_only
async def get_statistic(call: CallbackQuery, state: FSMContext, role: str):
    """ Колбэек на кнопку Стастистика """
    # print(f'Колл дата = {call.message.date.date()}')
    bot_logger.debug(f'State {await state.get_state()}')
    await call.message.edit_text(text="Выберите период", reply_markup=admin_stat_kb())
    await state.set_state(AdminMenuState.statistic_menu)


@admin_only
async def get_period_statistic(call: CallbackQuery, state: FSMContext, role: str):
    """
    Отображение календаря.
    Для создания календаря передаем список из дат за месяц и месяц в строковом формате
    Отображение календаря зависит от переданного CallbackQuery.
    call.data == 'stat_day' - передается календарь для выбора только за определенный день
    call.data == 'stat_all' - предлагается выбрать начальную дату периода

    """
    cal_btns_list = MyCalendar.current_date_list(call.message.date.date())
    month = MyCalendar.get_month_name(call.message.date.date())

    if call.data == 'stat_all':
        await call.message.edit_text(
            text='Выберите начальную дату периода', reply_markup=await calendar_kb(cal_btns_list, month)
        )

        await state.set_state(StatsState.waiting_first_date)
        bot_logger.debug(f'Выбор начальной даты периода: get_period_statistic {await state.get_state()}')

    if call.data == 'stat_day':
        await call.message.edit_text(
            text='Выберите дату', reply_markup=await calendar_kb(cal_btns_list, month)
        )

        await state.set_state(StatsState.waiting_date)
        bot_logger.debug(f'Выбор даты: get_period_statistic {await state.get_state()}')


@admin_only
async def day_statistic(call: CallbackQuery, state: FSMContext, role: str):
    """
    Сохранение даты в состояние day_date из CallbackQuery.
    Ответ по статистике из бд за определенный день
    :param call:
    :param state: answer
    :param role: admin
    """
    call_date = from_str_to_date_day(call.data)
    await state.update_data(day_date=call_date)

    data = await state.get_data()
    day = data.get('day_date')

    statistic = await get_statistic_from_db(day_date=day)

    bot_logger.debug(f'Получил статистику за день')
    if statistic:
        await call.message.edit_text(
            text=
            f'*Зарегистрировано новых пользователей*: `{statistic.new_user}`\n'
            f'*Просмотров бота за день `{call.data.split("_")[1]}`*: `{statistic.event}`',
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=back_button()
        )
    else:
        await call.message.edit_text(
            text=f'Не удалось получить данные, либо их нет.',
            reply_markup=back_button()
        )
    await state.set_state(StatsState.answer)


@admin_only
async def first_day_statistic(call: CallbackQuery, state: FSMContext, role: str):
    """
    Сохранение начальной даты в fitst_date.
    Выбор конечной даты периода для отображения статистики.
    """
    call_date = from_str_to_date_day(call.data)
    await state.update_data(first_date=call_date)  # сохраняем данные в сстояние fitst_date

    cal_btns_list = MyCalendar.current_date_list(call.message.date.date())
    month = MyCalendar.get_month_name(call.message.date.date())
    bot_logger.debug('жду конечную дату')
    await call.message.edit_text(
        text=f'Вы выбрали {call_date}\n'
             f'Теперь выберите конечную дату периода',
        reply_markup=await calendar_kb(cal_btns_list, month)
    )

    await state.set_state(StatsState.waiting_second_date)


@admin_only
async def second_day_statistic(call: CallbackQuery, state: FSMContext, role: str):
    """
    Отправляет ответ по статистике за выбранный период.
    :param call: CallbackQuery
    :param state: FSMContext
    :param role: admin
    :return: message
    """

    call_date = from_str_to_date_day(call.data)
    await state.update_data(second_date=call_date)
    data = await state.get_data()
    first_date = data.get('first_date')
    second_date = data.get('second_date')
    period = await get_statistic_from_db(first_date=first_date, second_date=second_date)
    if period:
        statistic = await answer_statistic_from_period(period)
        await call.message.edit_text(
            text=f'*В период с `{first_date}` по `{second_date}`*:\n'
                 f'*Зарегистрировано пользователей:* {statistic[0]}\n'
                 f'*Всего входов:* {statistic[1]}\n',
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=back_button()
        )
    else:
        await call.message.edit_text(
            text=f'Нет данных.',
            reply_markup=back_button()
        )
    # await state.clear_data()
    await state.set_state(StatsState.answer)


async def get_statistic_from_db(first_date: date = None,
                                second_date: date = None,
                                day_date: date = None):
    """
    Получение данных статистики из бд. Передаем параметры в зависимости от запроса (за день или за определенный период).
    :param first_date:
    :param second_date:
    :param day_date:
    :return: Статистика за день или указанный период
    """
    try:
        if day_date:
            day_statistic = await Statistic.get_or_none(day=day_date)
            bot_logger.debug(f'day_statistic: {day_statistic}')
            return day_statistic
        if first_date:
            period_statistic = await Statistic.filter(day__gte=first_date, day__lte=second_date)
            bot_logger.debug(f'period_statistic: {period_statistic}')
            return period_statistic

    except Exception as e:
        bot_logger.error(f'Ошибка во время получения статистики из бд, {e}')


async def answer_statistic_from_period(list_period: List[Statistic]) -> list:
    """
    Преобразовывает данные из статистики за период в список из суммы новых юзеров и суммы ивентов
    :param list_period: список из объектов бд Statistic
    :return: список из суммы зарегистрированных юзеров и суммы ивентов
    """
    sum_new_users = sum(statistic.new_user for statistic in list_period)
    sum_events = sum(statistic.event for statistic in list_period)
    return [sum_new_users, sum_events]
