from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.admin_keyboards import get_review_keyboard, admin_keyboard, review_kb
from keyboards.menu_keyboard import inline_menu_kb
from states.menu_states import MenuState
from utils.config import admin_id, get_admin_id
from database.models_db import AdminPost, Review
from utils.ai_generator import generate_ai_greeting
from utils.if_admin import is_admin
from utils.logging_config import bot_logger


async def show_admin_btn(message: Message):
    """ Вход в админ клавиатуру """
    bot_logger.info('Вход в админку')
    admin = await is_admin(message.from_user.id)
    if admin:
        await message.answer(text='Выберите действие',
                             reply_markup=admin_keyboard())
    else:
        await message.answer(text='У вас нет прав для этого действия.',
                             reply_markup=inline_menu_kb())


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
    await state.set_state(MenuState.review_menu)
    await call.message.edit_text('Отзывы пользователей',
                                 reply_markup=await review_kb())


async def moderate_review(call: CallbackQuery, state: FSMContext):
    """ Обработка отзыва пользователя """
    await state.set_state(MenuState.approve_menu)
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



# async def moderate_reviews(message: Message):
#     """ Модерация отзыва от пользователя """
#     admin_ids = get_admin_id()
#     if message.from_user.id not in admin_ids:
#         print(admin_id, type(admin_id), message.from_user.id, type(message.from_user.id))
#         await message.answer("У вас нет прав на модерацию.")
#         return
#
#     pending_reviews = await Review.filter(approved=False)
#
#     if not pending_reviews:
#         await message.answer("Нет отзывов на модерацию.")
#         return
#
#     for review in pending_reviews:
#         text = f"Отзыв от {review.first_name or 'пользователь'}:\n{review.text or ''}"
#         kb = get_review_keyboard(review.id)
#         if review.photo_file_id:
#             await asyncio.sleep(0.5)
#             await message.bot.send_photo(chat_id=admin_id, photo=review.photo_file_id, caption=text, reply_markup=kb)
#         else:
#             await message.bot.send_message(chat_id=admin_id, text=text, reply_markup=kb)



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
