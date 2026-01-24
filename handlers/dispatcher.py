from aiogram import Dispatcher, F
from aiogram.filters import Command, StateFilter

from config.middleware import RoleMiddleware, StatisticMiddleware
from config.settings_redis import redis_client

from handlers.admin.admin_rights_handlers import show_baristas_to_admin, delete_admin, save_role_admin, approve_admin, \
    show_admins_for_delete
from handlers.admin.barista_rights_handlers import barista_rights, start_register_name_barista, enter_role_barista, \
    save_barista_role, baristas_for_delete, delete_barista
from handlers.admin.get_statistic_handlers import get_statistic, get_period_statistic, day_statistic, \
    first_day_statistic, second_day_statistic, prev_month, next_month
from handlers.barista.add_game_handlers import add_game, add_title_game, add_description_game, add_date_game, \
    add_time_game, approve_game, add_image_game
from handlers.barista.barista_menu_handler import barista_menu, show_barista_menu_game, show_barista_posts_menu
from handlers.games.game_handlers import show_games_menu, show_games, show_one_game, registration_user_game, \
    show_old_games
from handlers.help_handlers import help_menu
from handlers.start_handlers import get_start, on_start
from handlers.admin.admin_handlers import admin_menu_handler, admin_menu

from handlers.barista.barista_handlers import (approve_review, reject_review, moderate_review,
                                               show_reviews, add_post, add_photo, save_post, generate_phrase,
                                               change_post, save_edited_text, show_barista_posts, barista_post)

from handlers.barista.user_review_handlers import (handle_review_photo, ask_for_photo, ask_for_text,
                                                   handle_review_text)
from handlers.back_handler import back, clear_message
from handlers.cancel_state_handler import cancel_handler
from handlers.horoscope_handkers import show_horoscope, send_horoscope, start_schedule_horo
from states.games_state import AddGameState

from states.menu_states import ReviewStates, PostState, StatsState, BaristaRegistrationState, AdminRegistrationState

from utils.shedulers.cleane_base_scheduler import horo_to_clean


def setup_dispatcher(dp: Dispatcher):
    """ Регистрация роутеров бота """
    dp.startup.register(on_start)
    # мидлвары
    dp.message.middleware(StatisticMiddleware(redis_client))
    dp.callback_query.middleware(StatisticMiddleware(redis_client))
    dp.message.middleware(RoleMiddleware())
    dp.callback_query.middleware(RoleMiddleware())

    # команды
    dp.message.register(get_start, Command(commands='start'))
    dp.message.register(cancel_handler, Command(commands='cancel'))
    dp.message.register(help_menu, Command(commands='help'))
    # панель администратора
    dp.callback_query.register(admin_menu, F.data == "admin_panel")
    dp.callback_query.register(admin_menu_handler, F.data == "admin")
    dp.callback_query.register(get_statistic, F.data == 'statistic')
    dp.callback_query.register(barista_rights, F.data == "rights")
    dp.callback_query.register(get_statistic, F.data == 'statistic')

    # добавление админа
    dp.callback_query.register(show_baristas_to_admin, F.data == 'add_admin')
    dp.callback_query.register(approve_admin, StateFilter(AdminRegistrationState.search_name))
    dp.callback_query.register(save_role_admin, StateFilter(AdminRegistrationState.waiting_choice))
    dp.callback_query.register(show_admins_for_delete, F.data == 'admins_for_delete')
    dp.callback_query.register(delete_admin, F.data.startswith('delete_'))

    # регистрация бариста
    dp.callback_query.register(start_register_name_barista, F.data == "add_barista")
    dp.message.register(enter_role_barista, StateFilter(BaristaRegistrationState.registration_name))
    dp.callback_query.register(save_barista_role,  StateFilter(BaristaRegistrationState.save_name))

    # удаление бариста
    dp.callback_query.register(baristas_for_delete, F.data == "baristas_for_delete")
    dp.callback_query.register(delete_barista, F.data.startswith("delete_"))

    # календарь
    dp.callback_query.register(get_period_statistic, F.data.startswith('stat_'))
    dp.callback_query.register(prev_month, F.data == "prev_month")
    dp.callback_query.register(next_month, F.data == "next_month")
    dp.callback_query.register(day_statistic, StateFilter(StatsState.waiting_date))
    dp.callback_query.register(first_day_statistic, StateFilter(StatsState.waiting_first_date))
    dp.callback_query.register(second_day_statistic, StateFilter(StatsState.waiting_second_date))

    # панель бариста
    dp.callback_query.register(barista_menu, F.data == 'barista')
    dp.callback_query.register(show_barista_menu_game, F.data == "games")
    dp.callback_query.register(show_barista_posts_menu, F.data == "posts")
    dp.callback_query.register(show_barista_posts, F.data == "barista_posts")
    dp.callback_query.register(show_reviews, F.data == "moderate")
    dp.callback_query.register(moderate_review, F.data.startswith("review_"))
    dp.callback_query.register(ask_for_photo, F.data == "share_photo")
    dp.callback_query.register(ask_for_text, F.data == "share_wish")
    dp.callback_query.register(approve_review, F.data.startswith("approve_"))
    dp.callback_query.register(reject_review, F.data.startswith("reject_"))
    dp.callback_query.register(barista_post, F.data.startswith("post_"))
    dp.callback_query.register(clear_message,  F.data.startswith('clear_'))

    # добавление поста
    dp.callback_query.register(add_post, F.data == "add_post")
    dp.message.register(add_photo, StateFilter(PostState.add_post))  # type: ignore[arg-type]
    dp.message.register(save_post, StateFilter(PostState.register_text))
    dp.message.register(save_edited_text, StateFilter(PostState.editing_text))
    dp.callback_query.register(generate_phrase, F.data == "generate_text")
    dp.callback_query.register(change_post, F.data == "change_text")
    dp.callback_query.register(save_post, F.data == "save_post")

    # панель юзера
    # панель гороскопа
    dp.callback_query.register(show_horoscope, F.data == "horoscope")
    dp.callback_query.register(send_horoscope, F.data.startswith('zodiac_'))
    dp.message.register(handle_review_photo, StateFilter(ReviewStates.waiting_for_photo))
    dp.message.register(handle_review_text, StateFilter(ReviewStates.waiting_for_text))
    dp.callback_query.register(horo_to_clean, F.data == 'stocks')

    # панель игр
    dp.callback_query.register(show_games_menu, F.data == 'games_all')
    dp.callback_query.register(show_games, F.data == 'show_upcoming_games')
    dp.callback_query.register(show_old_games, F.data == 'show_passed_games')
    dp.callback_query.register(show_one_game, F.data.startswith('game_'))
    dp.callback_query.register(registration_user_game,  F.data.startswith('register_for_game_'))

    # добавление игры
    dp.callback_query.register(add_game, F.data == 'add_game')
    dp.message.register(add_title_game, StateFilter(AddGameState.add_title))
    dp.message.register(add_description_game, StateFilter(AddGameState.add_description))
    dp.callback_query.register(add_date_game, StateFilter(AddGameState.add_date))
    dp.callback_query.register(add_time_game, StateFilter(AddGameState.add_time))
    dp.message.register(add_image_game, StateFilter(AddGameState.add_image))
    dp.callback_query.register(approve_game, StateFilter(AddGameState.save_game))

    dp.callback_query.register(back, F.data == 'back')

    # суперадмин
    dp.callback_query.register(start_schedule_horo, F.data == "start_horo")
    return dp
