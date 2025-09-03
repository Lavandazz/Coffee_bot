from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.admin_keyboards import admin_btn, admin_kb, admin_rights, admin_stat_kb
from keyboards.barista_keyboard import review_kb, edit_text_keyboard, barista_kb, barista_menu_kb, \
    barista_game_menu_kb
from keyboards.games_keyboard import games_kb
from keyboards.horoscope_keyboard import zodiac_kb
from keyboards.menu_keyboard import inline_menu_kb
from states.games_state import GameMenuState, AddGameState
from states.menu_states import MenuState, ReviewStates, AdminMenuState, BaristaState, PostState, StatsState, \
    BaristaRegistrationState, AdminRegistrationState

from utils.logging_config import bot_logger


async def back(call: CallbackQuery, state: FSMContext, bot: Bot, role: str):
    """
     Обработка кнопки 'Назад'.
     current_state - получаем текущее состояние из FSMContext и сравниваем с перечисленными состояниями
    :param call: CallbackQuery - необходим для изменения текста и клавиатуры
    :param state: Установка нового состояния
    :param bot: Глобальный экземпляр бота используется для отправки сообщения
    :param role:
    :return: text, kb
    """
    current_state = await state.get_state()
    bot_logger.debug(f'Начало обработки back. Текущее состояние: {current_state}')

    try:
        # возврат в главное меню
        if current_state in {MenuState.horoscope_menu.state, ReviewStates.waiting_for_photo.state,
                             ReviewStates.waiting_for_text.state, AdminMenuState.admin_menu.state,
                             MenuState.help_menu.state, GameMenuState.main_game_menu}:

            await call.message.edit_text("Главное меню", reply_markup=await inline_menu_kb(call.from_user.id))
            await state.clear()
            await state.set_state(MenuState.main_menu)
            bot_logger.info(f'Сброшено состояние {current_state} → главное меню')

        # переход в пользовательское в меню знаков зодиака
        elif current_state == MenuState.zodiac_menu.state:
            await state.set_state(MenuState.horoscope_menu)
            await call.message.edit_text("Выбери свой знак", reply_markup=zodiac_kb())
            bot_logger.info(f'Переход {current_state} → {MenuState.horoscope_menu}')

        # переход в главную админ-панель
        elif current_state in {AdminMenuState.admin.state, AdminMenuState.barista.state, BaristaState.menu}:
            await state.set_state(AdminMenuState.admin_menu)
            await call.message.edit_text("Вы находитесь в админ-панели.", reply_markup=admin_btn(role=role))
            bot_logger.info(f'Переход {current_state} → {AdminMenuState.admin_menu}')

        # переход в меню главное бариста с двумя кнопками (посты, игры)
        elif current_state in {BaristaState.posts_menu, BaristaState.games_menu}:
            await state.set_state(BaristaState.menu)
            await call.message.edit_text("Вы находитесь в меню бариста...", reply_markup=barista_menu_kb())
            bot_logger.info(f'Переход {current_state} → {BaristaState.menu}')

        # переход из постов/игр в посты
        elif current_state in {BaristaState.review_menu.state, BaristaState.posts.state, BaristaState.post.state,
                               PostState.add_post.state, PostState.register_text.state, PostState.editing_text.state,
                               PostState.save_post.state}:

            if current_state == PostState.add_post.state:
                await state.clear()
                bot_logger.info(f'Очищено состояние: {current_state}')

            await state.set_state(BaristaState.posts_menu)
            new_state = await state.get_state()
            await call.message.edit_text("Вы находитесь в разделе постов", reply_markup=barista_kb())
            bot_logger.info(f'Переход {current_state} → {new_state}')

        elif current_state == BaristaState.approve_menu.state:
            await state.set_state(BaristaState.review_menu)
            new_state = await state.get_state()
            try:
                await call.message.edit_text("Вы находитесь в меню бариста!..", reply_markup=barista_kb())
                bot_logger.info(f'Переход {current_state} → {new_state}')
            except TelegramBadRequest:
                await call.message.delete()
                await bot.send_message(chat_id=call.from_user.id, text="Вы находитесь в меню бариста...",
                                       reply_markup=await review_kb())
                bot_logger.warning(f'TelegramBadRequest при переходе {current_state} → {new_state}')

        elif current_state == PostState.editing_text.state:
            await state.set_state(PostState.save_post)
            new_state = await state.get_state()
            text = await state.get_data()
            ai_text = text.get('text')
            await call.message.edit_text(text=ai_text, reply_markup=edit_text_keyboard())
            bot_logger.info(f'Переход {current_state} → {new_state}. Ожидание ввода текста')

        # возврат в статистику
        elif current_state in {StatsState.waiting_date, StatsState.waiting_first_date,
                               StatsState.waiting_second_date, StatsState.answer}:
            await state.clear()
            await state.set_state(AdminMenuState.statistic_menu)
            new_state = await state.get_state()
            await call.message.edit_text(text='Возврат в статистику', reply_markup=admin_stat_kb())
            # await calendar_kb(call.message.date)
            bot_logger.info(f'Переход {current_state} → {new_state}')

        # возврат в админ меню
        elif current_state in {AdminMenuState.statistic_menu, AdminMenuState.rights}:
            await state.set_state(AdminMenuState.admin)
            new_state = await state.get_state()
            await call.message.edit_text(text='Возврат в меню', reply_markup=admin_kb())
            bot_logger.info(f'Переход {current_state} → {new_state}')

        # возврат в управление правами
        elif current_state in {BaristaRegistrationState.registration_name, BaristaRegistrationState.delete_name,
                               AdminRegistrationState.search_name, AdminRegistrationState.save_name,
                               AdminRegistrationState.delete_name}:

            await state.clear()
            await state.set_state(AdminMenuState.rights)
            new_state = await state.get_state()
            await call.message.edit_text(text='Возврат в управление правами', reply_markup=admin_rights())
            bot_logger.info(f'Очистка и переход {current_state} → {new_state}')

        # возврат в меню игр
        elif current_state in {GameMenuState.upcoming_game_menu, GameMenuState.past_game_menu}:
            await state.set_state(GameMenuState.main_game_menu)
            new_state = await state.get_state()
            await call.message.edit_text(text='Возврат в меню выбора игр', reply_markup=games_kb())
            bot_logger.info(f'Переход {current_state} → {new_state}')

        # возврат к меню выбора игр из описания игры
        elif current_state == GameMenuState.game:
            await call.message.delete()  # при удалении сообщения показывается предыдущее сообщение с клавиатурой

            # если data = new, то устанавливаем состояние "предстоящие игры"
            # иначе считаем что состояние "прошедшие игры"
            data = await state.get_data()
            if data.get("type_game") == "new":
                await state.set_state(GameMenuState.upcoming_game_menu)
            else:
                await state.set_state(GameMenuState.past_game_menu)
            # очищаем data
            await state.set_data({})

            new_state = await state.get_state()

            bot_logger.info(f'Очистка и переход {current_state} → {new_state}')

        # Добавление игры
        elif current_state in {AddGameState.add_title, AddGameState.save_game}:
            await state.clear()
            await state.set_state(GameMenuState.main_game_menu)
            new_state = await state.get_state()
            await call.message.edit_text(text="Выберите действие...", reply_markup=barista_game_menu_kb())
            bot_logger.info(f'Очистка и переход {current_state} → {new_state}')

        # Добавление игры (обработка сообщений)
        elif current_state in {AddGameState.add_description, AddGameState.add_image}:
            data = await state.get_data()
            await state.clear()
            await state.set_state(GameMenuState.main_game_menu)
            new_state = await state.get_state()

            if 'bot_message_id' in data:
                await bot.edit_message_text(chat_id=data['bot_chat_id'], message_id=data['bot_message_id'],
                                            text="Выберите действие.", reply_markup=barista_game_menu_kb())

            bot_logger.info(f'Очистка и переход {current_state} → {new_state}')

        else:
            bot_logger.warning(f'Необработанное состояние в back: {current_state}')

    except TelegramBadRequest as e:
        bot_logger.error(f'TelegramBadRequest при обработке back из состояния {current_state}: {e}')
        # Дополнительная обработка ошибки, если нужно
        raise

    except Exception as e:
        bot_logger.error(f'Ошибка при обработке back из состояния {current_state}: {e}')
        raise


async def clear_message(call: CallbackQuery, bot: Bot, role: str):
    """ Скрыть уведомление о новом отзыве """
    if role == 'barista':
        await call.message.delete()
        bot_logger.debug(f'Удалил сообщение')
