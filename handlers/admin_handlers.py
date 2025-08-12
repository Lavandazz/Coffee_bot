from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards.admin_keyboards import admin_btn, admin_kb, admin_stat_kb
from keyboards.calendar_keyboard import calendar_kb
from states.menu_states import AdminMenuState, StatsState
from utils.custom_calendar import MyCalendar
from utils.get_user import admin_only, staff_only
from utils.logging_config import bot_logger


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
    """
    await state.set_state(StatsState.waiting_second_date)
