from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.barista_keyboard import barista_keyboard, get_review_keyboard, review_kb
from keyboards.menu_keyboard import inline_menu_kb
from states.menu_states import AdminMenuState
from database.models_db import AdminPost, Review
from utils.ai_generator import generate_ai_greeting
from utils.if_admin import is_admin
from utils.logging_config import bot_logger


async def show_barista_btn(call: CallbackQuery, state: FSMContext, role: str):
    """ Вход в админ клавиатуру """
    bot_logger.info('Вход в панель бариста')
    await state.set_state(AdminMenuState.barista)
    if role == 'admin' or role == 'barista':
        await call.message.edit_text(text='Вы находитесь в меню бариста.',
                                     reply_markup=barista_keyboard())
    else:
        await call.message.edit_text(text='У вас нет прав для этого действия.',
                                     reply_markup=await inline_menu_kb(call.from_user.id))


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


async def show_reviews(call: CallbackQuery, state: FSMContext):
    """ Обработка кнопки Отзывы пользователей """
    bot_logger.info('отправлю клаву')
    await state.set_state(AdminMenuState.review_menu)
    await call.message.edit_text('Отзывы пользователей',
                                 reply_markup=await review_kb())


async def moderate_review(call: CallbackQuery, state: FSMContext):
    """ Обработка отзыва пользователя """
    await state.set_state(AdminMenuState.approve_menu)
    if not await is_admin(call.from_user.id):
        bot_logger.warning('недостаточно прав на модерацию отзыва')
        await call.answer("У вас нет прав на модерацию.")
        return

    review = await Review.get(id=call.data.split('_')[1])
    message = (f'Отзыв от {review.username}:\n\n'
               f'{review.text}')
    if review.photo_file_id:
        message += review.photo_file_id
    await call.message.edit_text(message, reply_markup=get_review_keyboard(review.id))


async def approve_review(callback: CallbackQuery):
    """ Размещение отзыва """
    review_id = int(callback.data.split("_")[1])
    review = await Review.get(id=review_id)
    review.approved = True
    await review.save()

    await callback.answer("Одобрено!")
    await callback.message.edit_reply_markup()


async def reject_review(callback: CallbackQuery, bot: Bot):
    """ Отклонение отзыва """
    review_id = int(callback.data.split("_")[1])
    await Review.get(id=review_id)

    await callback.answer("Отклонено!")
    # await bot.send_message()
    await callback.message.edit_reply_markup()
