from aiogram.fsm.state import StatesGroup, State


class MenuState(StatesGroup):
    main_menu = State()
    horoscope_menu = State()
    zodiac_menu = State()
    admin_menu = State()
