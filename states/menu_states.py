from aiogram.fsm.state import StatesGroup, State


class MenuState(StatesGroup):
    main_menu = State()
    horoscope_menu = State()
    zodiac_menu = State()


class AdminMenuState(StatesGroup):
    admin_menu = State()
    admin = State()
    barista = State()
    review_menu = State()
    approve_menu = State()


class ReviewStates(StatesGroup):
    waiting_for_photo = State()
    waiting_for_text = State()
