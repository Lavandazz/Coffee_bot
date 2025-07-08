from keyboards.admin_keyboards import admin_btn
from keyboards.horoscope_keyboard import zodiac_kb
from keyboards.menu_keyboard import inline_menu_kb
from .menu_states import MenuState, AdminMenuState, BaristaState, PostState, ReviewStates

TRANSITION_MAP = {
    'main_menu': {
        'states': {
            MenuState.horoscope_menu.state,
            ReviewStates.waiting_for_photo.state,
            ReviewStates.waiting_for_text.state,
            AdminMenuState.admin_menu.state
        },
        'target_state': MenuState.main_menu,
        'text': 'Главное меню',
        'keyboard': lambda call: inline_menu_kb(call.from_user.id),
        'clear_state': True
    },
    'admin': {
        'states': {
            AdminMenuState.admin.state,
            AdminMenuState.barista.state
        },
        'target_state': AdminMenuState.admin_menu,
        'text': 'Админ-панель',
        'get_keyboard': lambda role: admin_btn(role=role),
        'clear_state': False
    },
    'barista': {
        'states': {
            BaristaState.review_menu.state,
            BaristaState.approve_menu.state,
            PostState.save_post.state
        },
        'target_state': AdminMenuState.admin_menu,
        'text': 'Админ-панель',
        'get_keyboard': lambda role: admin_btn(role=role),
        'clear_state': False
    },
    'zodiac': {
        'states': {
            MenuState.zodiac_menu.state,
        },
        'target_state': MenuState.horoscope_menu,
        'text': 'Админ-панель',
        'get_keyboard': zodiac_kb(),
        'clear_state': False
    }

}

