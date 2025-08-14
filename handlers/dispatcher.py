from aiogram import Dispatcher, F
from aiogram.filters import Command, StateFilter

from handlers.help_handlers import help_menu
from handlers.start_handlers import get_start, on_start
from handlers.admin_handlers import (admin_menu_handler, admin_menu, get_statistic, get_period_statistic)

from handlers.barista_handlers import approve_review, reject_review, moderate_review, show_barista_btn, show_reviews, \
    add_post, add_photo, save_post, generate_phrase, change_post, save_edited_text, show_barista_posts, barista_post

from handlers.user_review_handlers import (handle_review_photo, ask_for_photo, ask_for_text,
                                           handle_review_text)
from handlers.back_handler import back, clear_message
from handlers.cancel_state_handler import cancel_handler
from handlers.horoscope_handkers import show_horoscope, send_horoscope, start_schedule_horo

from states.menu_states import ReviewStates, PostState, StatsState
from utils.middleware import RoleMiddleware, StatisticMiddleware
from utils.shedulers.cleane_base_scheduler import horo_to_clean
from utils.config import redis_client


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
    # календарь
    # dp.callback_query.register(get_day_statistic, F.data == 'stat_day')
    dp.callback_query.register(get_period_statistic, F.data.startswith('stat_'))
    # dp.include_router(calendar_dialog)
    # setup_dialogs(dp)

    # панель бариста
    dp.callback_query.register(show_barista_btn, F.data == "barista")
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

    dp.callback_query.register(back, F.data == 'back')
    # суперадмин
    dp.callback_query.register(start_schedule_horo, F.data == "start_horo")
    return dp
