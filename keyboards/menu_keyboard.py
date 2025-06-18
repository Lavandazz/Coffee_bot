from aiogram.utils.keyboard import InlineKeyboardBuilder


def inline_menu_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='Поделиться фото', callback_data='share_photo')
    kb.button(text='Поделиться пожеланием', callback_data='share_wish')
    kb.button(text='Кофейный гороскоп', callback_data='horoscope')
    kb.button(text='Акции', callback_data='stocks')
    kb.adjust(2)

    return kb.as_markup()
