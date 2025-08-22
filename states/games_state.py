from aiogram.fsm.state import StatesGroup, State


class GameMenuState(StatesGroup):
    """ Главное меню"""
    main_game_menu = State()
    upcoming_game_menu = State()
    past_game_menu = State()
    future_game = State()
    past_game = State()
