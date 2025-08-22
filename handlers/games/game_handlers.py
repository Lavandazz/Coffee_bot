from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.models_db import Game
from keyboards.games_keyboard import games_kb, show_games_kb
from states.games_state import GameMenuState
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
    отображаем список предстоящих или прошедших игр
    """
    bot_logger.debug(f'показываю игры')
    if call.data == "show_upcoming_games":
        games = await Game.filter(status='to be').all()
        if games:
            await call.message.edit_text(
                text='Какую игру выберешь ты?',
                reply_markup=await show_games_kb(games)

            )
        else:
            await call.message.edit_text(
                text='Игры пока не назначены. Но мы стараемся выбрать самую интересную',
                reply_markup=await show_games_kb(games)
            )
        await state.set_state(GameMenuState.upcoming_game_menu)

    elif call.data == "show_passed_games":
        games = await Game.filter(status='pass').all()
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
