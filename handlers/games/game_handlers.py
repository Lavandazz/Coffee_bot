from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.models_db import Game, User
from keyboards.back_keyboard import back_button
from keyboards.games_keyboard import games_kb, show_games_kb, game_registration_kb
from states.games_state import GameMenuState
from utils.config import bot
from utils.logging_config import bot_logger


async def show_games_menu(call: CallbackQuery, state: FSMContext):
    """
    Отображение меню игр (предстоящие/завершенные)
    """
    await call.message.edit_text(
        text='Побывать в кофейне, это не только попить кофе,'
             'Это про настроение, новые знакомства.\n'
             'Поэтому, предлагаем вам ознакомиться с предстоящими играми.',
        reply_markup=games_kb()
    )
    await state.set_state(GameMenuState.main_game_menu)


async def show_games(call: CallbackQuery, state: FSMContext):
    """
    Отображение всех предстоящих игр.
    В зависимости от CallbackQuery (upcoming_games/past_games)
    отображаем список предстоящих или прошедших игр.
    В state.data сохраняем message_id как ключ game_menu для того, чтобы в дальнейшем обратиться
    к этому сообщению и изменить его.
    """
    if call.data == "show_upcoming_games":
        games = await Game.filter(status='to be').all()
        if games:
            await call.message.edit_text(
                text='Какую игру выберешь ты?',
                reply_markup=await show_games_kb(games)
            )
            await state.update_data(game_menu=call.message.message_id)
        else:
            await call.message.edit_text(
                text='Игры пока не назначены. Но мы стараемся выбрать самую интересную',
                reply_markup=await show_games_kb(games)
            )
        await state.set_state(GameMenuState.upcoming_game_menu)


async def show_old_games(call: CallbackQuery, state: FSMContext):
    """
    Отображение прошедших игр.
    Игры отображаются как кнопки
    """
    try:
        # получаем список объектов Game до текущей даты (текущая не входит)
        games = await Game.filter(date_game__lt=call.message.date).all()
        if games:
            await call.message.edit_text(
                text="Прошедшие игры",
                reply_markup=await show_games_kb(games)
            )
        else:
            await call.message.edit_text(
                text='Ничего не найдено.',
                reply_markup=await show_games_kb(games)
            )

        await state.set_state(GameMenuState.past_game_menu)

    except Exception as e:
        bot_logger.error(f'Не удалось отправить клавиатуру с прошедшими играми: {e}')
        await call.message.edit_text(text='Произошла ошибка. Попробуйте позже',
                                     reply_markup=games_kb())


async def show_one_game(call: CallbackQuery, state: FSMContext):
    """
    После выбора игры отображается фото игры и полное описание с кнопками:
    Записаться на игру / Назад
    """
    status = ""
    call_game = call.data.split('_')[1]
    await state.set_state(GameMenuState.game)

    if call.message.text.startswith("Какую игру"):
        status = "new"
        # сохраняем состояние в data как статус
        # для дальнейших переходов из просмотра игры в правильное состояние
        await state.update_data(type_game=status)

    try:
        game = await Game.filter(id=call_game).first()
        if game:
            await bot.send_photo(
                chat_id=call.message.chat.id,
                photo=game.image,
                caption=f'Приглашаем вас посетить игру:\n'
                f'{game.title}.\n'
                f'{game.description}.\n'
                f'Дата: {game.date_game}.\n'
                f'Время: {game.time_game}',
                reply_markup=game_registration_kb(game_id=game.id, status=status)
                )
            # Сохраняем message_id в state
            mess = call.message.message_id
            await state.update_data(photo_message_id=mess)

            bot_logger.debug(f'сохранил {mess}')

    except Exception as e:
        bot_logger.error(f'не удалось отправить описание игры: {e}')
        await call.message.edit_text(text='Произошла ошибка. Попробуйте позже',
                                     reply_markup=games_kb())


async def registration_user_game(call: CallbackQuery, state: FSMContext):
    """
    Регистрация пользователя на игру.
    Если нажата кнопка Записаться на игру (register_for_game_), происходит проверка записан ли игрок.
    Если игрок не записан, отправляется сообщение о записи и запись в бд.
    Сообщение с фото удаляется и изменяется клавиатура game_menu.

    :param call:
    :param state:
    :return:
    """
    if call.data.startswith("register_for_game_"):
        game_id = call.data.split('_')[3]
        game = await Game.get(id=game_id)
        user = await User.get(telegram_id=call.from_user.id)

        message = await make_answer(user=user, game=game)
        data = await state.get_data()

        await call.message.delete()

        await bot.edit_message_text(text=message,
                                    chat_id=call.from_user.id,
                                    message_id=data.get('game_menu'),
                                    reply_markup=games_kb())

        # устанавливаем состояния
        # для дальнейшего перехода в главное меню
        await state.set_state(GameMenuState.main_game_menu)


async def make_answer(user: User, game: Game) -> str:
    """
    Регистрация пользователя на игру.
    Если пользователь уже зарегистрирован, то создается соответствующее сообщение и повторной записи не происходит.
    Если пользователь еще не зарегистрирован в игре, происходит запись в бд, возвращается сообщение о ней.
    :param user: Объект модели User
    :param game: Объект модели Game
    :return: text-str
    """

    exist = await Game.filter(id=game.id, players__id=user.id).exists()

    if not exist:
        await game.players.add(user)
        message = (f"✅ ОК!\n"
                   f"Вы записаны на игру {game.title}\n"
                   f"{game.date_game} в {game.time_game}")
    else:
        message = f"⚠️ Вы уже записаны на эту игру."

    return message
