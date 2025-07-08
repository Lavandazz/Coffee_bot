from datetime import datetime

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.back_keyboard import back_button
from keyboards.barista_keyboard import (barista_keyboard, get_review_keyboard, review_kb, get_post_keyboard,
                                        edit_text_keyboard, barista_posts_kb)
from keyboards.menu_keyboard import inline_menu_kb
from states.menu_states import AdminMenuState, BaristaState, PostState
from database.models_db import Review, AdminPost, User
from utils.ai_generator import generate_ai_greeting

from utils.get_user import is_admin, get_users_from_db
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


async def add_post(call: CallbackQuery, state: FSMContext, role: str):
    """ Загрузка файла и текста от бариста """
    await state.set_state(BaristaState.add_post)
    await call.message.edit_text('📤 Отправьте фото кофе с подписью (или просто фото)')
    await state.set_state(PostState.register_photo)


async def add_photo(message: Message, state: FSMContext, role: str):
    """ Загрузка файла и текста от бариста """
    if not message.photo:
        await message.answer("Пожалуйста, отправьте фото!")
        return
    photo = message.photo[-1]  # Берём самое большое изображение
    text = message.caption  # Текст под фото (может быть None)

    await state.update_data(photo=photo, text=text)

    if not text:
        # Если текста нет, предлагаем ввести или генерируем автоматически
        await message.answer(
            "☕ Вы не добавили подпись. Хотите, чтобы я придумал её за вас?",
            reply_markup=get_post_keyboard()
        )
    else:
        # Если текст есть, сохраняем пост
        await message.answer('Выберите действие', reply_markup=edit_text_keyboard())


async def generate_phrase(call: CallbackQuery, state: FSMContext):
    """ Обработка кнопки для генерации текста поста """
    await call.message.edit_text('Ждите, генерирую фразу...')
    # ai_text = await generate_ai_greeting()
    ai_text = "Хорошего дня тебя, кофейный человек"
    await state.update_data(text=ai_text)
    print(ai_text)
    await call.message.edit_text(f'✨ Вот что я придумал:\n\n {ai_text}',
                                 reply_markup=edit_text_keyboard())


async def change_post(call: CallbackQuery, state: FSMContext, role: str):
    """ Обработка кнопки для редактирования текста сгенерированного поста """
    data = await state.get_data()
    current_text = data.get('text', "Текст не найден")
    await call.message.edit_text(
        f"✏️ <b>Текущий текст:</b>\n\n{current_text}\n\n"
        "Отправьте новый текст или нажмите 'Назад'",
        reply_markup=back_button(),  # Кнопка для отмены
        parse_mode="HTML"
    )
    await state.set_state(PostState.editing_text)  # Ждём новый текст


async def save_edited_text(message: Message, state: FSMContext):
    # Сохраняем новый текст в состоянии
    await state.set_state(PostState.save_post)
    await state.update_data(text=message.text)
    # Показываем обновлённый вариант
    data = await state.get_data()
    await message.answer(
        f"✅ <b>Обновлённый текст:</b>\n\n{data['text']}, "
        f"Фото: {data['register_photo']}",
        reply_markup=edit_text_keyboard(),  # Кнопки "Сохранить" и "Править ещё"
        parse_mode="HTML"
    )
    await state.set_state(PostState.generated_text)  # Возвращаемся к состоянию подтверждения


async def save_post(call: CallbackQuery, state: FSMContext, bot: Bot):
    """ Загрузка файла и текста от бариста """
    post_data = await state.get_data()
    photo = post_data.get('photo')
    photo_file_id = photo.file_id

    text = post_data.get('text')
    date = call.message.date.date()
    print(date, text)

    if not text:
        text = await generate_ai_greeting()

    if not photo_file_id:
        await call.message.answer("Ошибка: фото не найдено!")
        return

    await state.set_state(PostState.save_post)
    # сохранение в бд
    await to_save(photo_file_id, text, call.from_user.id)

    await bot.send_photo(chat_id=call.message.chat.id,
                         photo=photo_file_id,
                         caption=f'Отлично!\n'f'Публикую пост:\n'
                                 f'{text}',
                         reply_markup=back_button())


async def to_save(photo: str, text: str, user_id: int):
    """ Сохранение поста бариста"""
    user = await User.get(telegram_id=user_id)
    await AdminPost.create(
        user_id=user,
        photo_file_id=photo,
        text=text
    )


async def show_reviews(call: CallbackQuery, state: FSMContext, role: str):
    """ Обработка кнопки Отзывы пользователей """
    bot_logger.info('отправлю клаву')
    await state.set_state(BaristaState.review_menu)
    reviews = await Review.filter(approved=False).only("id", "created_at")

    if reviews:
        await call.message.edit_text('Отзывы пользователей',
                                     reply_markup=await review_kb(reviews))
    else:
        await call.message.edit_text('Отзывов нет',
                                     reply_markup=back_button())


async def moderate_review(call: CallbackQuery, state: FSMContext, role: str):
    """ Обработка отзыва пользователя """
    await state.set_state(BaristaState.approve_menu)
    baristas = await get_users_from_db('barista')
    baristas = [barista.get('telegram_id') for barista in baristas]
    if not (call.from_user.id in baristas
            ):
        bot_logger.warning('недостаточно прав на модерацию отзыва')
        await call.answer("У вас нет прав на модерацию.")
        return

    review = await Review.get(id=call.data.split('_')[1])
    message = (f'Отзыв от {review.username}:\n\n'
               f'{review.text}')
    await call.message.edit_text(message, reply_markup=get_review_keyboard(review.id))
    if review.photo_file_id:
        message += review.photo_file_id
        await call.message.edit_text(message, reply_markup=get_review_keyboard(review.id))


async def answer_for_review(call: CallbackQuery, status: bool, role: str):
    """ Сохранение отзыва"""
    review_id = int(call.data.split("_")[1])
    review = await Review.get(id=review_id)
    user = await review.user
    telegram_id = user.telegram_id
    review.approved = status
    await review.save()
    return telegram_id


async def approve_review(call: CallbackQuery, bot: Bot, role: str, state: FSMContext):
    """ Размещение отзыва """
    telegram_id = await answer_for_review(call, True, role)
    current_state = await state.get_state()
    print(current_state)
    await call.answer("Одобрено!")
    # await call.message.delete()
    if await state.get_state() == BaristaState.approve_menu:
        bot_logger.debug(f'Проверка статуса {current_state}')
        await call.message.edit_text(
            "Вы находитесь в меню бариста...",
            reply_markup=barista_keyboard()
        )
    await bot.send_message(chat_id=telegram_id, text='Ваш отзыв одобрен')


async def reject_review(call: CallbackQuery, bot: Bot, role: str, state: FSMContext):
    """ Отклонение отзыва """
    telegram_id = await answer_for_review(call, True, role)
    await call.answer("Отклонено!")
    if await state.get_state() == BaristaState.approve_menu:
        await call.message.edit_text(
            "Вы находитесь в меню бариста...",
            reply_markup=barista_keyboard()
        )
    await call.message.delete()
    await bot.send_message(chat_id=telegram_id, text='Ваш отзыв отклонен')


async def show_barista_posts(call: CallbackQuery, state: FSMContext, role: str):
    """ Отображение всех постов бариста """
    await state.set_state(BaristaState.posts)
    await call.message.edit_text(text=f'Выберите пост', reply_markup=await barista_posts_kb())

