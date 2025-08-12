import datetime
import locale

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Calendar


from database.models_db import Statistic
from handlers.back_handler import back
from keyboards.admin_keyboards import admin_btn, admin_kb, admin_stat_kb
from keyboards.back_keyboard import back_button
from keyboards.calendar_keyboard import calendar_kb

from keyboards.menu_keyboard import inline_menu_kb
from states.menu_states import MenuState, AdminMenuState, StatsState
from utils.custom_calendar import MyCalendar
from utils.get_user import admin_only, staff_only

from utils.logging_config import bot_logger


locale.setlocale(locale.LC_TIME, 'Russian_Russia.1251')


@staff_only
async def admin_menu(call: CallbackQuery, state: FSMContext, role: str):
    """ Отображение клавиатуры админ-панели """
    await state.set_state(AdminMenuState.admin_menu)
    await call.message.edit_text(text='Вы вошли в админ-панель', reply_markup=admin_btn(role=role))


@admin_only
async def admin_menu_handler(call: CallbackQuery, state: FSMContext, role: str):
    """ Вход в админ клавиатуру """
    bot_logger.info('Вход в панель админа')
    await state.set_state(AdminMenuState.admin)
    await call.message.edit_text(text='Меню администратора',
                                 reply_markup=admin_kb())


@admin_only
async def get_statistic(call: CallbackQuery, state: FSMContext, role: str):
    """ Колбэек на кнопку Стастистика """
    await state.set_state(AdminMenuState.statistic_menu)
    # print(f'Колл дата = {call.message.date.date()}')
    bot_logger.debug(f'State {await state.get_state()}')
    await call.message.edit_text(text="Выберите период", reply_markup=admin_stat_kb())


@admin_only
async def get_period_statistic(call: CallbackQuery, state: FSMContext, role: str):
    """
    Отображение календаря.
    Для создания календаря передаем список из дат за месяц и месяц в строковом формате
    Отображение календаря зависит от переданного CallbackQuery.
    call.data == 'stat_day' - передается календарь для выбора только за определенный день
    call.data == 'stat_all' - предлагается выбрать начальную дату периода

    """

    if call.data == 'stat_all':
        await state.set_state(StatsState.waiting_first_date)
        cal_btns_list = MyCalendar.current_date_list(call.message.date.date())
        month = MyCalendar.get_month_name(call.message.date.date())
        await call.message.edit_text(
            text='Выберите начальную дату периода', reply_markup=await calendar_kb(cal_btns_list, month)
        )
        bot_logger.debug(f'Выбор начальной даты периода: get_period_statistic {await state.get_state()}')

    if call.data == 'stat_day':
        await state.set_state(StatsState.waiting_date)
        cal_btns_list = MyCalendar.current_date_list(call.message.date.date())
        month = MyCalendar.get_month_name(call.message.date.date())
        await call.message.edit_text(
            text='Выберите дату', reply_markup=await calendar_kb(cal_btns_list, month)
        )
        bot_logger.debug(f'Выбор даты: get_period_statistic {await state.get_state()}')

@admin_only
async def choice_period_statistic(call: CallbackQuery, state: FSMContext, role: str, month: str):
    """
    Выбор конечной даты периода для отображения статистики.
    :param call:
    :param state:
    :param role:
    :return:
    """
    await state.set_state(StatsState.waiting_second_date)



# @admin_only
# async def get_day_statistic(call: CallbackQuery, widget,
#                             manager: DialogManager, selected_date: datetime.date, state: FSMContext, role: str):
#     """Обработка статистики за один день"""
#     await state.set_state(StatsState.waiting_date)
#     await state.update_data(is_period=False)
#
#     # await call.message.edit_text(
#     #     text='Введите дату в формате: "01.01.2025" (день, месяц, год)',
#     #     reply_markup=back_button()
#     # )
#     bot_logger.debug(f'State {await state.get_state()}')
#
#
#
# @admin_only
# async def get_period_statistic(call: CallbackQuery, state: FSMContext, role: str):
#     """Обработка статистики за период"""
#     await state.set_state(StatsState.waiting_first_date)
#     await call.message.edit_text(
#         text='Введите начальную дату периода в формате: "01.01.2025" (день, месяц, год)',
#         reply_markup=back_button()
#     )
#     bot_logger.debug(f'State {await state.get_state()}')
#
#
# @admin_only
# async def process_first_date(message: Message, state: FSMContext, role: str):
#     """Обработка первой даты периода"""
#     try:
#         date = parse_date(message.text)
#         await state.update_data(first_date=date)
#         await state.set_state(StatsState.waiting_second_date)
#         await message.answer(
#             'Введите конечную дату периода в том же формате: "01.01.2025" (день, месяц, год)',
#             reply_markup=back_button()
#         )
#         bot_logger.debug(f'State {await state.get_state()}')
#     except ValueError:
#         await message.answer('Неверный формат даты. Попробуйте снова.')
#
#
# @admin_only
# async def process_second_date(message: Message, state: FSMContext, role: str):
#     """Обработка второй даты периода и вывод статистики"""
#     try:
#         data = await state.get_data()
#         first_date = data['first_date']
#         second_date = parse_date(message.text)
#
#         if second_date < first_date:
#             raise ValueError("Конечная дата должна быть после начальной")
#
#         stats = await Statistic.filter(
#             day__gte=first_date,
#             day__lte=second_date
#         ).order_by('day')
#
#         bot_logger.debug(f'State {await state.get_state()}')
#
#         await message.answer(
#             text=format_stats_message(stats, period=True),
#             reply_markup=back_button()
#         )
#         await state.set_state(AdminMenuState.statistic)
#     except ValueError as e:
#         await message.answer(f'Ошибка: {str(e)}. Попробуйте снова.')
#
#
# @admin_only
# async def process_single_date(message: Message, state: FSMContext, role: str):
#     """Обработка даты для статистики за один день"""
#     try:
#         date = parse_date(message.text)
#         stat = await Statistic.get_or_none(day=date)
#
#         await message.answer(
#             text=format_stats_message(stat, period=False),
#             reply_markup=back_button()
#         )
#         await state.set_state(AdminMenuState.statistic)
#         bot_logger.debug(f'State {await state.get_state()}')
#     except ValueError:
#         await message.answer('Неверный формат даты. Попробуйте снова.')
#
#
# def parse_date(date_str: str) -> datetime.date:
#     """Парсинг даты из строки"""
#     try:
#         import re
#         # Преобразуем строку в дату
#         date_text = re.sub(r'[-.,: ]', ' ', date_str).split()
#         day, month, year = map(int, date_text)
#         return datetime.date(year, month, day)
#     except (ValueError, AttributeError):
#         raise ValueError("Неверный формат даты")
#
#
# def format_stats_message(stats: Statistic | list[Statistic], period: bool) -> str:
#     """Форматирование сообщения со статистикой"""
#     if not stats:
#         return "Нет данных за выбранный период"
#
#     if period:
#         message = "Статистика за период:\n\n"
#         total_events = 0
#         total_new_users = 0
#
#         for stat in stats:
#             message += (
#                 f"Дата: {stat.day.strftime('%Y-%m-%d')}\n"
#                 f"Посещений: {stat.event}\n"
#                 f"Новых пользователей: {stat.new_user}\n\n"
#             )
#             total_events += stat.event
#             total_new_users += stat.new_user
#
#         message += (
#             f"Итого за период:\n"
#             f"Всего посещений: {total_events}\n"
#             f"Всего новых пользователей: {total_new_users}"
#         )
#     else:
#         message = (
#             f"Статистика за {stats.day.strftime('%Y-%m-%d')}:\n"
#             f"Всего посещений: {stats.event}\n"
#             f"Новых пользователей: {stats.new_user}"
#         )
#     return message
