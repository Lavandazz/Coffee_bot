from aiogram import Dispatcher, F
from aiogram.filters import Command

from handlers.admin_handlers import approve_review, reject_review, moderate_reviews
from handlers.all_handlers import (on_start, get_start, handle_review_photo, ask_for_photo, ask_for_text,
                                   handle_review_text, show_horoscope, send_horoscope, start_schedule_horo)
from handlers.back_handler import back
from handlers.cancel_state_handler import cancel_handler
from utils.states import ReviewStates


def setup_dispatcher(dp: Dispatcher):
    """ Регистрация роутеров бота """
    dp.startup.register(on_start)
    dp.message.register(get_start, Command(commands='start'))
    dp.message.register(cancel_handler, Command(commands='cancel'))
    dp.callback_query.register(ask_for_photo, F.data == "share_photo")
    dp.callback_query.register(ask_for_text, F.data == "share_wish")
    dp.callback_query.register(show_horoscope, F.data == "horoscope")
    dp.callback_query.register(send_horoscope, F.data.startswith('zodiac_'))
    dp.message.register(handle_review_photo, ReviewStates.waiting_for_photo)
    dp.message.register(handle_review_text, ReviewStates.waiting_for_text)
    dp.callback_query.register(approve_review, F.data.startswith("approve_"))
    dp.callback_query.register(reject_review, F.data.startswith("reject_"))
    dp.message.register(moderate_reviews, F.text == "/moderate")
    dp.callback_query.register(start_schedule_horo,  F.data == "start_horo")
    dp.callback_query.register(back, F.data == 'back_to_menu')
    dp.callback_query.register(back, F.data == 'back')

    return dp
