import asyncio
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.models_db import Review, User
from keyboards.barista_keyboard import get_review_keyboard
from keyboards.back_keyboard import back_button
from keyboards.menu_keyboard import inline_menu_kb

from states.menu_states import ReviewStates

from utils.config import get_admin_id
from utils.logging_config import bot_logger


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
    data = await state.get_state()
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
    admin_ids = get_admin_id()

    try:
        for admin in admin_ids:
            bot_logger.info(f"Попытка отправки фото админу {admin} ({type(admin)})")
            await bot.send_message(
                admin,
                f"🆘 Новый фотоотзыв #{review.id}\n"
                f"От: @{message.from_user.username}\n"
                f"Сообщение: {caption}\n",
                # f"Сообщение: {message.photo}",
                reply_markup=get_review_keyboard(review.id)
            )

    except Exception as e:
        bot_logger.exception(f"💥 Ошибка при отправке сообщения админу : {e}")

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

    admin_ids = get_admin_id()

    try:
        for admin in admin_ids:
            await asyncio.sleep(0.5)
            bot_logger.info(f"Попытка отправки админу {admin} ({type(admin)})")
            await bot.send_message(
                admin,
                f"🆘 Новый текстовый отзыв #{review.id}\n"
                f"От: @{message.from_user.username}\n"
                f"Сообщение: {message.text}",
                reply_markup=get_review_keyboard(review.id)
            )

    except Exception as e:
        bot_logger.exception(f"💥 Ошибка при отправке сообщения админу : {e}")

    await message.answer(text="Спасибо за отзыв! Бариста его рассмотрит ☕",
                         reply_markup=await inline_menu_kb(message.from_user.id))
    await state.clear()
