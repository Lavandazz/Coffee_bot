from aiogram.utils.keyboard import InlineKeyboardBuilder


def back_button():
    """ Кнопка назад """
    kb = InlineKeyboardBuilder()
    kb.button(text='⬅️ Назад', callback_data='back')
    kb.adjust(1)
    return kb.as_markup()
