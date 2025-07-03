from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.admin_keyboards import admin_keyboard, admin_btn
from keyboards.barista_keyboard import barista_keyboard
from keyboards.menu_keyboard import inline_menu_kb
from states.menu_states import MenuState, AdminMenuState
from database.models_db import AdminPost, Review
from utils.ai_generator import generate_ai_greeting
from utils.if_admin import is_admin
from utils.logging_config import bot_logger


async def admin_menu(call: CallbackQuery, state: FSMContext, role: str):
    """ Отображение клавиатуры админ-панели """
    await state.set_state(AdminMenuState.admin_menu)
    await call.message.edit_text(text='Вы вошли в админ-панель', reply_markup=admin_btn(role=role))


async def admin_menu_handler(call: CallbackQuery, state: FSMContext, role: str):
    """ Вход в админ клавиатуру """
    bot_logger.info('Вход в панель админа')
    await state.set_state(AdminMenuState.admin)
    if role == 'admin':
        await call.message.edit_text(text='Вы в меню администратора',
                                     reply_markup=admin_keyboard())
    else:
        await call.message.edit_text(text='У вас нет прав для этого действия.',
                                     reply_markup=await inline_menu_kb(call.from_user.id))
