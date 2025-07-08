from aiogram.fsm.state import StatesGroup, State


class MenuState(StatesGroup):
    main_menu = State()
    horoscope_menu = State()
    zodiac_menu = State()


class AdminMenuState(StatesGroup):
    admin_menu = State()
    admin = State()
    barista = State()


class BaristaState(StatesGroup):
    review_menu = State()
    approve_menu = State()
    add_post = State()
    posts = State()


class PostState(StatesGroup):
    add_post = State()
    register_photo = State()
    register_text = State()
    generated_text = State()
    editing_text = State()
    save_post = State()


class ReviewStates(StatesGroup):
    waiting_for_photo = State()
    waiting_for_text = State()
