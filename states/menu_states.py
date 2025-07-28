from aiogram.fsm.state import StatesGroup, State


class MenuState(StatesGroup):
    """ Главное меню"""
    main_menu = State()
    horoscope_menu = State()
    zodiac_menu = State()
    admin_menu = State()
    help_menu = State()


class AdminMenuState(StatesGroup):
    """ Меню админа """
    admin_menu = State()
    admin = State()
    barista = State()
    statistic_menu = State()  # меню статистики
    statistic = State()


class StatsState(StatesGroup):
    waiting_date = State()
    waiting_first_date = State()
    waiting_second_date = State()



class BaristaState(StatesGroup):
    """ Меню бариста """
    review_menu = State()
    approve_menu = State()
    posts = State()  # отображение всех постов
    post = State()  # отображение поста


class PostState(StatesGroup):
    """ Действия, связанные с регистрацией поста """
    add_post = State()  # добавление поста
    register_text = State()  # добавление текста
    generated_text = State()  # генерация текста AI
    editing_text = State()  # изменение текста поста
    save_post = State()  # сохранение поста


class ReviewStates(StatesGroup):
    """ Добавление отзыва клиентом """
    waiting_for_photo = State()
    waiting_for_text = State()
