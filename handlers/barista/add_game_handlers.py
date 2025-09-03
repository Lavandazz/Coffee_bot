import asyncio
from datetime import datetime, date

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from tortoise.exceptions import DoesNotExist

from database.models_db import User, Game
from keyboards.admin_keyboards import yes_or_no_btn
from keyboards.back_keyboard import back_button
from keyboards.barista_keyboard import barista_game_menu_kb
from keyboards.calendar_keyboard import calendar_kb
from keyboards.hour_keyboard import hour_kb
from states.games_state import AddGameState, GameMenuState
from states.menu_states import AdminMenuState, BaristaState
from utils.config import bot
from utils.custom_calendar import MyCalendar
from utils.date_formats import from_str_to_date_day, date_game_saver
from utils.get_user import staff_only
from utils.logging_config import bot_logger

GAME = {}
NEW_DATE = date.today()


@staff_only
async def add_game(call: CallbackQuery, state: FSMContext, role: str):
    """
    Колбек на кнопку 'Добавить игру'.
    Отправляет запрос на сохранения названия игры и сохраняет state add_title
    """
    await call.message.edit_text(
        text=f'Введите название игры\n'
             f'Для отмены введите команду /cancel',
        reply_markup=back_button()
    )
    await state.set_state(AddGameState.add_title)


@staff_only
async def add_title_game(message: Message, state: FSMContext, role: str):
    """
    Ожидание ввода названия игры и сохранение в state title
    """
    if not message.text:
        await message.answer("Пожалуйста, отправьте название игры!", reply_markup=back_button())
        return

    await state.update_data(title=message.text.strip())

    sent_message = await message.answer(
        text=f'Отлично! Теперь введите описание игры.\n'
             f'Для отмены введите команду /cancel',
        reply_markup=back_button()
    )
    # Сохраняем данные для будущего удаления
    await state.update_data(
        bot_message_id=sent_message.message_id,
        bot_chat_id=message.from_user.id
    )
    await state.set_state(AddGameState.add_description)


@staff_only
async def add_description_game(message: Message, state: FSMContext, role: str):
    """
    Ожидание ввода описания игры и сохранение в state add_description.
    Отправляет календарь на текущий месяц для выбора даты игры
    """
    global NEW_DATE

    NEW_DATE = message.date
    if not message.text:
        await message.answer("Пожалуйста, отправьте описание игры!", reply_markup=back_button())
        return

    await state.update_data(description=message.text.strip())
    bot_logger.debug(f'Получено описание игры')

    await message.answer(
        text=f'Отлично! Теперь выберите дату игры.\n'
             f'Для отмены введите команду /cancel',
        reply_markup=await calendar_kb(NEW_DATE)
    )

    await state.set_state(AddGameState.add_date)


@staff_only
async def add_date_game(call: CallbackQuery, state: FSMContext, role: str):
    """
    Ожидание ввода даты игры и сохранение в state add_date
    """
    global NEW_DATE
    await call_back_menu(call=call, state=state)  # возврат в меню если нажата кнопка Назад

    if call.data.startswith('day_'):
        call_date = from_str_to_date_day(call.data)

        try:
            while not date_game_saver(call_date):
                await call.answer(
                    text=f'❕ Дата игры не может быть раньше текущей даты.\n',
                    show_alert=False)

                await call.message.edit_text(
                    text=f'Выберите корректную дату',
                    reply_markup=await calendar_kb(NEW_DATE)
                )
                return

            else:
                # Если дата корректная, обрабатываем как обычно
                await state.update_data(date_game=call_date)
                await state.set_state(AddGameState.add_time)
                bot_logger.debug(f'Получил дату игры {call_date}, тип {type(call_date)}')

                await call.message.edit_text(
                    text='Почти закончили. Осталось выбрать время игры.\n',
                    reply_markup=hour_kb()

                )
        except TelegramBadRequest as e:
            if "message is not modified" in str(e).lower():
                # При повторном нажатии на ту же старую дату
                await call.answer(
                    text='❕ Дата игры не может быть раньше текущей даты.',
                    show_alert=False
                )

        except Exception as e:
            bot_logger.error(f"Неожиданная ошибка в add_date_game: {e}")

            await call.answer("Произошла ошибка", show_alert=True)


@staff_only
async def add_time_game(call: CallbackQuery, state: FSMContext, role: str):
    """
    Ожидание ввода времени игры и сохранение в state add_time.
    Преобразовывает полученное время из str в time.
    Сохраняем отправляемое сообщение в sent_message, айди этого сообщения и чат юзера, чтобы обратиться
    к этим данным и изменить сообщение отправив новую клавиатуру (при условии нажатия на кнопку Назад).
    """

    await state.set_state(AddGameState.add_image)
    if call.data.startswith('time_'):
        time = call.data.split('_')[1]
        time_game = datetime.strptime(time, '%H:%M').time()

        await state.update_data(time_game=time_game)
        sent_message = await call.message.edit_text(
            text=f"Последние штрихи 🫶 \n"
                 f"Добавьте изображение нажав на скрепку ниже ⤵️",
            reply_markup=back_button()
        )
        # сохраняем айди сообщения и юзера для дальнейшего изменения при нажатии на кнопку Назад
        await state.update_data(
            bot_message_id=sent_message.message_id,
            bot_chat_id=call.from_user.id
        )

    else:
        await call_back_menu(call=call, state=state)  # возврат в меню если нажата кнопка Назад


@staff_only
async def add_image_game(message: Message, bot: Bot, state: FSMContext, role: str):
    """
    Загрузка изображения.
    Отправляет сообщение автору о том, какой текст будет сохранен.
    Отправляет клавиатуру для подтверждения сохранения информации об игре.
    """
    if not message.photo:
        await message.answer("Пожалуйста, отправьте фото!", reply_markup=back_button())
        return
    image = message.photo[-1]  # Берём самое большое изображение

    await state.update_data(image=image)

    # получаем все данные из state.data
    data = await state.get_data()
    title = data['title']
    description = data['description']
    date_game = data['date_game']
    time_game = data['time_game']
    image = data['image']
    image_id = image.file_id
    bot_logger.debug(f'Передаю в сохранение time_game {time_game}, date_game {date_game}')

    data_game(title=title, description=description, date=date_game, time_game=time_game, image=image_id,
              author_id=message.from_user.id)

    await bot.send_photo(chat_id=message.from_user.id,
                         caption=f'Анонсированный текст:\n'
                         f'ВНИМАНИЕ‼️\n'
                         f'Игра начинается❗️\n'
                         f'{title}\n'
                         f'{description}\n'
                         f'Дата: {date_game}\n'
                         f'Время: {time_game}',
                         photo=image_id,
                         reply_markup=yes_or_no_btn()
                         )
    await state.set_state(AddGameState.save_game)


@staff_only
async def approve_game(call: CallbackQuery, state: FSMContext, role: str):
    """
    Функция подтверждения описания игры.
    Если будет нажата кнопка YES, то перейдет к сохранению в бд.
    NO вернет в меню игр.
    """
    curr_state = await state.get_state()
    bot_logger.debug(f'текущий статус {curr_state}')

    if call.data == 'yes':
        user_id = await User.get(telegram_id=call.from_user.id)
        # Сохраняем игру в БД
        await save_game(
            title=GAME.get('title'),
            description=GAME.get('description'),
            date_game=GAME.get('date_game'),
            time_game=GAME.get('time_game'),
            image=GAME.get('image'),
            author_id=user_id.id  # добавляем автора
        )
        # await call.answer(text='✔️ Игра сохранена')
        await call.message.delete()
        await asyncio.sleep(1)
        await bot.send_message(
            chat_id=call.from_user.id,
            text='✔️ Игра сохранена\nВозврат в меню:',
            reply_markup=barista_game_menu_kb())

    elif call.data == 'no':
        await call.message.delete()
        await asyncio.sleep(1)
        await call.message.answer(
            text='❌Данные не сохранены',
            reply_markup=barista_game_menu_kb()
        )
    await state.clear()
    await state.set_state(BaristaState.games_menu)


def data_game(title: str, description: str, date: datetime.date, time_game: datetime.time, image: str, author_id: int):
    GAME['title'] = title
    GAME['description'] = description
    GAME['date_game'] = date
    GAME['time_game'] = time_game
    GAME['image'] = image
    GAME['author_id'] = author_id
    return GAME


async def save_game(title: str, description: str,
                    date_game: datetime.date, time_game: datetime, image: str, author_id: int):
    """
    Сохранение игры в бд
    """
    bot_logger.debug('Начинается сохранение игры')
    bot_logger.debug(f'author_id: {author_id}, title: {title}, description: {description}, '
                     f'date: {time_game}, time_game: {time_game}')

    try:
        author = await User.get(id=author_id)
        bot_logger.debug(f'author = {author}, author_id = {author_id}, author_tele = {author.telegram_id}\n'
                         f'image = {image}')
        # Создаем игру
        game = await Game.create(
            title=title,
            description=description,
            date_game=date_game,
            time_game=time_game,
            image=image,  # или ваша логика для изображения
            user=author,  # передаем в сохранение не User.id, а объект User целиком
            status='to be',
            text='game'
        )
        await game.players.add(author)  # добавляем автора игры в игру
        bot_logger.info(f"Игра '{title}' создана пользователем {author_id}")
    except DoesNotExist:
        bot_logger.error(f"Пользователь не найден: {author_id}")
        raise
    except Exception as e:
        bot_logger.error(f"Ошибка: {e}")
        raise


async def call_back_menu(call: CallbackQuery, state: FSMContext):
    """
    Возврат в меню игр и сброс состояния.
    Новое состояние присваивается GameMenuState.main_game_menu
    :param state: GameMenuState.main_game_menu
    :return: barista_game_menu_kb()
    """
    if call.data == "back":
        await state.clear()
        await state.set_state(GameMenuState.main_game_menu)
        await call.message.edit_text(
            text=f'Возврат в меню игр',
            reply_markup=barista_game_menu_kb())

        return


def make_message(title: str, description: str, date: str, time_game: str):
    pass
