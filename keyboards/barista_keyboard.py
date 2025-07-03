from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models_db import Review
from utils.logging_config import bot_logger


def barista_keyboard():
    """ Кнопки в отделе администрирования """
    kb = InlineKeyboardBuilder()
    kb.button(text="Добавить пост",
              callback_data="add_post")
    kb.button(text="Отзывы пользователей",
              callback_data="moderate"),
    kb.button(text="Посты бариста",
              callback_data="barista_posts")
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))
    return kb.as_markup()


async def review_kb():
    """ Кнопки с отзывами от клиентов """
    kb = InlineKeyboardBuilder()
    reviews = await Review.filter(approved=False).only("id", "created_at")
    if not reviews:
        kb.button(text="Нет отзывов", callback_data="no_reviews")
        return kb.as_markup()

    for review in reviews:
        date = review.created_at.strftime("%d.%m.%Y")
        kb.button(text=f'{date}',
                  callback_data=f'review_{review.id}')
    kb.adjust(3)

    kb.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back'))  # добавляем отдельную кнопку в самый низ
    bot_logger.info('отправлена клавиатура с отзывами')
    return kb.as_markup()


def get_review_keyboard(review_id: int):
    """ Клавиатура для одобрения/отклонения отзыва """
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Одобрить", callback_data=f"approve_{review_id}")
    kb.button(text="❌ Отклонить", callback_data=f"reject_{review_id}")
    kb.button(text='⬅️ Назад', callback_data='back')
    kb.adjust(3)
    return kb.as_markup()
