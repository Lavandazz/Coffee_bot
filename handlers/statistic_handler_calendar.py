import locale
from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
# from aiogrаыam_dialog import DialogManager, Window, Dialog, StartMode
from aiogram_dialog.widgets.kbd import Calendar, CalendarConfig
from aiogram_dialog.widgets.text import Const

from states.calendar_states import MyCalendar
from utils.get_user import admin_only

# locale.setlocale(locale.LC_TIME, 'Russian_Russia.1251')

# @admin_only
# async def get_day_statistic(call: CallbackQuery, dialog_manager: DialogManager, state: FSMContext, role: str):
#     """Обработка статистики за один день"""
#     await dialog_manager.start(MyCalendar.choosing_date, mode=StartMode.NORMAL)
#
#
# async def on_date_selected(call: CallbackQuery, widget, manager: DialogManager, selected_date):
#     await call.message.answer(f"Вы выбрали дату: {selected_date.strftime('%d.%m.%Y')}")
#     await manager.done()
#
#
# # Окно календаря
# calendar_window = Window(
#     Const("Выберите дату:"),
#     Calendar(id="calendar", on_click=on_date_selected, config=CalendarConfig()),
#     state=MyCalendar.choosing_date,
# )
#
# # Сам диалог
# calendar_dialog = Dialog(calendar_window)
