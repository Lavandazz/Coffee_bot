from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from states.constants import TRANSITION_MAP
from utils.logging_config import bot_logger


class BackHandler:
    def __init__(self, call: CallbackQuery, state: FSMContext, role: str):
        self.call = call
        self.state = state
        self.role = role

    async def handle(self):
        """ Обработка кнопки 'Назад' """
        current_state = self.state.get_state()
        bot_logger.debug(f'Текущее состояние: {current_state}')
        for now_state in TRANSITION_MAP.values():
            if current_state in now_state.get('states'):
                pass

