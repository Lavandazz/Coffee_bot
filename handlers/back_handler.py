import asyncio
from dataclasses import dataclass
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery

from keyboards.admin_keyboards import admin_btn, admin_kb, admin_stat_kb, admin_rights
from keyboards.barista_keyboard import review_kb, edit_text_keyboard, barista_posts_kb, barista_kb
from keyboards.games_keyboard import games_kb
from keyboards.horoscope_keyboard import zodiac_kb
from keyboards.menu_keyboard import inline_menu_kb
from states.games_state import GameMenuState
from states.menu_states import MenuState, ReviewStates, AdminMenuState, BaristaState, PostState, StatsState, \
    BaristaRegistrationState, AdminRegistrationState
from utils.get_user import get_role_user
from utils.logging_config import bot_logger


async def back(call: CallbackQuery, state: FSMContext, bot: Bot, role: str):
    """ Обработка кнопки 'Назад' """
    current_state = await state.get_state()  # получаем текущее состояние

    # возврат в главное меню
    if current_state in {MenuState.horoscope_menu.state, ReviewStates.waiting_for_photo.state,
                         ReviewStates.waiting_for_text.state, AdminMenuState.admin_menu.state,
                         MenuState.help_menu.state,
                         GameMenuState.main_game_menu}:
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

    # возврат в статистику
    if current_state in (StatsState.waiting_date,
                         StatsState.waiting_first_date,
                         StatsState.waiting_second_date,
                         StatsState.answer
                         ):
        await state.set_state(AdminMenuState.statistic_menu)
        await call.message.edit_text(text='Возврат в статистику', reply_markup=admin_stat_kb())

    # возврат в админ меню
    if current_state in (AdminMenuState.statistic_menu,
                         AdminMenuState.rights):
        await state.set_state(AdminMenuState.admin)
        await call.message.edit_text(text='Возврат в статистику', reply_markup=admin_kb())
        bot_logger.debug(f'Новый статус {current_state}')

    # возврат в управление правами
    if current_state in (BaristaRegistrationState.registration_name,
                         BaristaRegistrationState.delete_name,
                         AdminRegistrationState.search_name,
                         AdminRegistrationState.save_name,
                         AdminRegistrationState.delete_name
                         ):
        bot_logger.debug(f'Статус {current_state} сбрасываю')
        await state.clear()

        await call.message.edit_text(text='Возврат в управление правами', reply_markup=admin_rights())
        await state.set_state(AdminMenuState.rights)
        bot_logger.debug(f'Новый статус {current_state}')

    # возврат в меню игр
    if current_state in (GameMenuState.upcoming_game_menu,
                         GameMenuState.past_game_menu):
        await state.set_state(GameMenuState.main_game_menu)
        await call.message.edit_text(
            text='Возврат в меню выбора игр',
            reply_markup=games_kb()
        )


async def clear_message(call: CallbackQuery, bot: Bot, role: str):
    """ Скрыть уведомление о новом отзыве """
    if role == 'barista':
        await call.message.delete()
        bot_logger.debug(f'Удалил сообщение')








