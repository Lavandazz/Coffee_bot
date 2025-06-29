import asyncio

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from datetime import datetime, timezone

from database.horoscope import MockHoroscope
from database.models_db import Review, User, Horoscope

from keyboards.admin_keyboards import get_review_keyboard
from keyboards.horoscope_keyboard import zodiac_kb, back_button
from keyboards.menu_keyboard import inline_menu_kb

from states.menu_states import MenuState

from utils.ai_generator import generate_day_or_night
from utils.config import get_admin_id
from utils.generate_horoscope import generate_coffee_horoscope
from utils.logging_config import bot_logger
from utils.schedulers import generate_horo
from utils.states import ReviewStates


async def on_start(bot: Bot):
    """ Отправка сообщения о старте админу """
    await bot.send_message(484385628, text='Я запустил CoffeeBot')


async def get_start(message: Message, bot: Bot):
    """ Старт приложения """
    time_message = message.date
    # Преобразуем часовой пояс (+3 часа для Москвы)
    local_time = time_message.replace(tzinfo=timezone.utc).astimezone(tz=None)  # Автоматически определит локальный пояс
    user_id = await User.filter(telegram_id=message.from_user.id).exists()  # проверка айди в базе
    if not user_id:
        await User.create(
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            telegram_id=message.from_user.id,
            is_admin=False)
        bot_logger.info(f'Зарегистрирован новый пользователь {message.from_user.id}')
    await bot.send_message(message.from_user.id,
                           f"{generate_day_or_night(local_time.hour)}",
                           reply_markup=inline_menu_kb())


async def ask_for_photo(call: CallbackQuery, state: FSMContext):
    """ Обработка кнопки Поделиться фото """
    await call.message.edit_text(f"Отправьте фото для отзыва ☕\n"
                                 f"Для отмены введите команду /cancel")
    await state.set_state(ReviewStates.waiting_for_photo)


async def ask_for_text(call: CallbackQuery, state: FSMContext):
    """ Обработка кнопки Поделиться отзывом """
    await call.message.edit_text(f"Напишите текст для отзыва ☕\n"
                                 f"Для отмены введите команду /cancel")

    await state.set_state(ReviewStates.waiting_for_text)


async def handle_review_photo(message: Message, state: FSMContext, bot: Bot):
    """ Загрузка отзыва с фото от пользователя """
    file_id = message.photo[-1].file_id
    caption = message.caption

    review = await Review.create(
        user_id=message.from_user.id,
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
                f"Сообщение: {message.photo}",
                reply_markup=get_review_keyboard(review.id)
            )

    except Exception as e:
        bot_logger.exception(f"💥 Ошибка при отправке сообщения админу : {e}")
    await message.answer("Спасибо за отзыв с фото! Бариста его рассмотрит ☕")
    await state.clear()


async def handle_review_text(message: Message, state: FSMContext, bot: Bot):
    """ Загрузка текстового отзыва от пользователя """
    # data = await state.get_data()
    review = await Review.create(
        user_id=message.from_user.id,
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

    await message.answer("Спасибо за отзыв! Бариста его рассмотрит ☕")
    await state.clear()


async def show_horoscope(call: CallbackQuery, state: FSMContext):
    """ Отображение знаков зодиака в клавиатуре """
    await state.set_state(MenuState.horoscope_menu)
    await call.message.edit_text('Выбери свой знак', reply_markup=zodiac_kb())


async def send_horoscope(call: CallbackQuery, state: FSMContext):
    """ Обработка кнопки знака зодиака """
    call_date = call.message.date.date()
    zodiac = call.data.replace('zodiac_', '')
    await state.set_state(MenuState.zodiac_menu)
    # получаем гороскоп их псевдобазы
    horoscope = await Horoscope.get_or_none(zodiac=zodiac, date=call_date)
    if horoscope:
        await call.message.edit_text(f'Гороскоп на сегодня: {horoscope.text}',
                                     reply_markup=back_button())

    else:
        horoscope = await MockHoroscope.get_or_none(zodiac, call_date.month)
        await call.message.edit_text(f'Гороскоп на сегодня: {horoscope.get("text")}',
                                     reply_markup=back_button())


async def start_schedule_horo(call: CallbackQuery):
    await call.answer('Запускаю гороскоп')
    await generate_horo()

