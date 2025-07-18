import asyncio
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.models_db import Review, User
from keyboards.barista_keyboard import get_review_keyboard
from keyboards.back_keyboard import back_button
from keyboards.menu_keyboard import inline_menu_kb

from states.menu_states import ReviewStates
from utils.get_user import get_users_from_db

from utils.logging_config import bot_logger
from utils.send_messages import SendMessage


async def ask_for_photo(call: CallbackQuery, state: FSMContext):
    """ Обработка кнопки Поделиться фото """
    await call.message.edit_text(f"Отправьте фото для отзыва ☕\n"
                                 f"Для отмены введите команду /cancel\n"
                                 f"Или нажмите на кнопку Назад",
                                 input_field_placeholder="Нажмите на кнопку скрепки 📎",
                                 reply_markup=back_button())
    await state.set_state(ReviewStates.waiting_for_photo)


async def ask_for_text(call: CallbackQuery, state: FSMContext):
    """ Обработка кнопки Поделиться отзывом """
    await call.message.edit_text(f"Оставьте отзыв ☕\n"
                                 f"Для отмены введите команду /cancel\n"
                                 f"Или нажмите на кнопку Назад",
                                 input_field_placeholder="Введите текст",
                                 reply_markup=back_button())

    await state.set_state(ReviewStates.waiting_for_text)


async def handle_review_photo(message: Message, state: FSMContext, bot: Bot):
    """ Загрузка отзыва с фото от пользователя """
    await state.get_state()
    file_id = message.photo[-1].file_id
    caption = message.caption
    user = await User.get(telegram_id=message.from_user.id)
    review = await Review.create(
        user=user,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        photo_file_id=file_id,
        text=caption
    )
    sender = SendMessage(user_role='barista', user=user, bot=bot, review_id=review.id, text=caption, file_id=file_id)
    await sender.send_message()

    await message.answer(text="Спасибо за отзыв с фото! Бариста его рассмотрит ☕",
                         reply_markup=await inline_menu_kb(message.from_user.id))
    await state.clear()


async def handle_review_text(message: Message, state: FSMContext, bot: Bot):
    """ Загрузка текстового отзыва от пользователя """
    user = await User.get(telegram_id=message.from_user.id)
    review = await Review.create(
        user=user,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        text=message.text
    )

    sender = SendMessage(user_role='barista', user=user, bot=bot, review_id=review.id, text=message.text)
    await sender.send_message()
    await message.answer(text="Спасибо за отзыв! Бариста его рассмотрит ☕",
                         reply_markup=await inline_menu_kb(message.from_user.id))
    await state.clear()
