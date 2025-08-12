from aiogram.fsm.state import StatesGroup, State


class MyCalendar(StatesGroup):
    choosing_date = State()
