from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.admin_keyboards import review_kb, admin_keyboard
from keyboards.horoscope_keyboard import zodiac_kb
from keyboards.menu_keyboard import inline_menu_kb
from states.menu_states import MenuState, ReviewStates
from utils.logging_config import bot_logger


async def back(call: CallbackQuery, state: FSMContext):
    """ Обработка кнопки 'Назад' """
    current_state = await state.get_state()  # получаем текущее состояние

    if (
            current_state == MenuState.horoscope_menu.state
            or current_state == ReviewStates.waiting_for_photo.state
            or current_state == ReviewStates.waiting_for_text.state
    ):
        # переход в пользовательское главное меню
        await state.set_state(MenuState.main_menu)  # Меняем состояние на "в меню"
        await call.message.edit_text("Главное меню", reply_markup=inline_menu_kb())
        await state.clear()
        bot_logger.info(f'Состояние {current_state} сброшено')

    # переход в пользовательское в меню знаков зодиака
    if current_state == MenuState.zodiac_menu.state:
        await state.set_state(MenuState.horoscope_menu)
        await call.message.edit_text("Выбери свой знак", reply_markup=zodiac_kb())

    # переход в меню администратора
    if current_state == MenuState.review_menu.state:
        await state.set_state(MenuState.admin_menu)
        await call.message.edit_text("Вы находитесь в меню администратора.",
                                     reply_markup=admin_keyboard())
        await state.clear()

    if current_state == MenuState.approve_menu.state:
        await state.set_state(MenuState.admin_menu)
        await call.message.edit_text("Выберите отзыв для модерации: ",
                                     reply_markup=await review_kb())

    # if current_state == ReviewStates.waiting_for_photo.state or current_state == ReviewStates.waiting_for_text.state:
    #     await state.set_state(MenuState.main_menu)  # Меняем состояние на "в меню"
    #     await call.message.edit_text("Главное меню", reply_markup=inline_menu_kb())
    #     await state.clear()

