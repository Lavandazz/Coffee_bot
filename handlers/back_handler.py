from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.horoscope_keyboard import zodiac_kb
from keyboards.menu_keyboard import inline_menu_kb
from states.menu_states import MenuState


async def back(call: CallbackQuery, state: FSMContext):
    """ Обработка кнопки 'Назад' """
    current_state = await state.get_state()  # получаем текущее состояние

    if current_state == MenuState.horoscope_menu.state:
        await state.set_state(MenuState.main_menu)  # Меняем состояние на "в меню"
        await call.message.edit_text("Главное меню", reply_markup=inline_menu_kb())
        await state.clear()
    if current_state == MenuState.zodiac_menu.state:
        await state.set_state(MenuState.horoscope_menu)  # Меняем состояние на "в меню"
        await call.message.edit_text("Главное меню", reply_markup=zodiac_kb())

    else:
        # Если состояние неизвестно — просто возвращаем в меню
        await call.message.edit_text(
            "Главное меню:",
            reply_markup=inline_menu_kb()
        )
