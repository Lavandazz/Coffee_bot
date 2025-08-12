import asyncio

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.back_handler_menu import BackHandler
from keyboards.admin_keyboards import admin_btn, admin_kb, admin_stat_kb
from keyboards.barista_keyboard import review_kb, edit_text_keyboard, barista_posts_kb, barista_kb
from keyboards.horoscope_keyboard import zodiac_kb
from keyboards.menu_keyboard import inline_menu_kb
from states.menu_states import MenuState, ReviewStates, AdminMenuState, BaristaState, PostState, StatsState
from utils.get_user import get_role_user
from utils.logging_config import bot_logger


async def back(call: CallbackQuery, state: FSMContext, bot: Bot, role: str):
    """ Обработка кнопки 'Назад' """
    current_state = await state.get_state()  # получаем текущее состояние

    if current_state in {MenuState.horoscope_menu.state, ReviewStates.waiting_for_photo.state,
                         ReviewStates.waiting_for_text.state, AdminMenuState.admin_menu.state,
                         MenuState.help_menu.state}:
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
    elif current_state in {BaristaState.review_menu.state,
                           BaristaState.posts.state,
                           BaristaState.post.state,
                           PostState.add_post.state,
                           PostState.register_text.state,
                           PostState.editing_text.state,
                           PostState.save_post.state}:
        bot_logger.debug(f'Текущее состояние {current_state}')

        try:
            if current_state == PostState.add_post.state:

                bot_logger.info(f'Состояние {current_state} очищено')
                await state.clear()

            await state.set_state(AdminMenuState.barista)
            await call.message.edit_text(
                "Вы находитесь в меню бариста",
                reply_markup=barista_kb()
            )
            bot_logger.debug(f'Перешел назад к состоянию {await state.get_state()}')

        # Блок except, т.к. пост отображается как фото и edit_text в этом случае не работает
        except TelegramBadRequest:
            await call.message.delete()
            await bot.send_message(chat_id=call.message.chat.id, text="Вы находитесь в меню бариста...",
                                   reply_markup=barista_kb()
            )
            bot_logger.info(f'Состояние {current_state} сброшено')

    elif current_state == BaristaState.approve_menu.state:

        await state.set_state(BaristaState.review_menu)
        try:
            await call.message.edit_text(
                "Вы находитесь в меню бариста!..",
                reply_markup=barista_kb()
            )
            bot_logger.info(f'Состояние {current_state}.')
        except TelegramBadRequest:
            await call.message.delete()
            await bot.send_message(chat_id=call.from_user.id, text="Вы находитесь в меню бариста...",
                                   reply_markup=await review_kb())

    if current_state == PostState.editing_text.state:
        await state.set_state(PostState.save_post)
        text = await state.get_data()
        ai_text = text.get('text')
        await call.message.edit_text(text=ai_text,
                                     reply_markup=edit_text_keyboard())
        bot_logger.debug(f'Состояние {current_state} Ожидание ввода текста для поста бариста')

    if current_state in (StatsState.waiting_date,
                         StatsState.waiting_first_date,
                         StatsState.waiting_second_date
                         ):
        await state.set_state(AdminMenuState.statistic_menu)
        await call.message.edit_text(text='Возврат в статистику', reply_markup=admin_stat_kb())

    if current_state == AdminMenuState.statistic_menu:
        await state.set_state(AdminMenuState.admin)
        await call.message.edit_text(text='Возврат в статистику', reply_markup=admin_kb())


async def clear_message(call: CallbackQuery, bot: Bot, role: str):
    """ Скрыть уведомление о новом отзыве """
    if role == 'barista':
        await call.message.delete()
        bot_logger.debug(f'Удалил сообщение')

# async def back(call: CallbackQuery, state: FSMContext):
#     # Получаем роль пользователя
#     role = await get_role_user(call.from_user.id)
#     handler = BackHandler(call, state, role)
#     await handler.handle()

