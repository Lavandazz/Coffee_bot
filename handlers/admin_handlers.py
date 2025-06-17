import asyncio
import time

from aiogram.types import Message, CallbackQuery

from keyboards.admin_keyboards import get_review_keyboard
from utils.config import admin_id, get_admin_id
from database.models_db import AdminPost, Review
from utils.ai_generator import generate_ai_greeting


async def handle_photo(message: Message):
    """ Загрузка файла и текста от бариста """
    file_id = message.photo[-1].file_id
    caption = message.caption

    # Если нет подписи — пробуем ИИ (пока просто заглушка)
    if not caption:
        caption = await generate_ai_greeting()

    await AdminPost.create(
        file_id=file_id,
        caption=caption
    )

    await message.answer("Фото с приветствием сохранено!")


async def moderate_reviews(message: Message):
    """ Модерация отзыва от пользователя """
    admin_ids = get_admin_id()
    if message.from_user.id not in admin_ids:
        print(admin_id, type(admin_id), message.from_user.id, type(message.from_user.id))
        await message.answer("У вас нет прав на модерацию.")
        return

    pending_reviews = await Review.filter(approved=False)

    if not pending_reviews:
        await message.answer("Нет отзывов на модерацию.")
        return

    for review in pending_reviews:
        text = f"Отзыв от {review.first_name or 'пользователь'}:\n{review.text or ''}"
        kb = get_review_keyboard(review.id)
        if review.photo_file_id:
            await asyncio.sleep(1)
            await message.bot.send_photo(chat_id=admin_id, photo=review.photo_file_id, caption=text, reply_markup=kb)
        else:
            await message.answer(text, reply_markup=kb)


async def approve_review(callback: CallbackQuery):
    """ Размещение отзыва """
    review_id = int(callback.data.split("_")[1])
    review = await Review.get(id=review_id)
    review.approved = True
    await review.save()

    await callback.answer("Одобрено!")
    await callback.message.edit_reply_markup()


async def reject_review(callback: CallbackQuery):
    """ Отклонение отзыва """
    review_id = int(callback.data.split("_")[1])
    review = await Review.get(id=review_id)
    await review.delete()

    await callback.answer("Отклонено!")
    await callback.message.edit_reply_markup()
