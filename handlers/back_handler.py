from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.admin_keyboards import admin_keyboard, admin_btn
from keyboards.barista_keyboard import barista_keyboard, review_kb, edit_text_keyboard
from keyboards.horoscope_keyboard import zodiac_kb
from keyboards.menu_keyboard import inline_menu_kb
from states.menu_states import MenuState, ReviewStates, AdminMenuState, BaristaState, PostState
from utils.logging_config import bot_logger


async def back(call: CallbackQuery, state: FSMContext, role: str):
    """ Обработка кнопки 'Назад' """
    current_state = await state.get_state()  # получаем текущее состояние

    if current_state in {MenuState.horoscope_menu.state, ReviewStates.waiting_for_photo.state,
                         ReviewStates.waiting_for_text.state, AdminMenuState.admin_menu.state}:
        # переход в пользовательское главное меню
        await state.set_state(MenuState.main_menu)  # Меняем состояние на "в меню"
        await call.message.edit_text("Главное меню", reply_markup=await inline_menu_kb(call.from_user.id))
        await state.clear()
        bot_logger.debug(f'Состояние {current_state} сброшено')

    # переход в пользовательское в меню знаков зодиака
    elif current_state == MenuState.zodiac_menu.state:
        await state.set_state(MenuState.horoscope_menu)
        await call.message.edit_text("Выбери свой знак", reply_markup=zodiac_kb())

    # переход в главную админ-панель
    elif (
            current_state == AdminMenuState.admin.state or
            current_state == AdminMenuState.barista.state
    ):
        await state.set_state(AdminMenuState.admin_menu)
        await call.message.edit_text("Вы находитесь в админ-панели.",
                                     reply_markup=admin_btn(role=role))
        bot_logger.debug(f'Состояние {current_state} сброшено')

    # переход в меню бариста
    elif current_state in {BaristaState.review_menu.state, PostState.save_post.state,
                           BaristaState.posts}:
        await state.set_state(AdminMenuState.barista)
        try:
            await call.message.edit_text(
                "Вы находитесь в меню бариста...",
                reply_markup=barista_keyboard()
            )
            bot_logger.info(f'Состояние {current_state} сброшено')

        except TelegramBadRequest:
            await call.message.edit_caption(
                caption="Вы находитесь в меню бариста.....",
                reply_markup=barista_keyboard()
            )
            bot_logger.debug(f'Состояние {current_state} сброшено')

    elif current_state == BaristaState.approve_menu.state:
        await state.set_state(BaristaState.review_menu)
        await call.message.edit_text(
            "Вы находитесь в меню бариста...",
            reply_markup=await review_kb()
        )
        bot_logger.info(f'Состояние {current_state} сброшено')

    if current_state == PostState.editing_text.state:
        await state.set_state(PostState.save_post)
        text = await state.get_data()
        ai_text = text.get('text')
        await call.message.edit_text(text=ai_text,
                                     reply_markup=edit_text_keyboard())
        bot_logger.debug(f'Состояние {current_state} сброшено')




