from aiogram.fsm.state import State, StatesGroup

class ReviewStates(StatesGroup):
    waiting_for_photo = State()
    waiting_for_text = State()
