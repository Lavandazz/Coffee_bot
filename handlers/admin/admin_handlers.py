from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.admin_keyboards import admin_btn, admin_kb
from states.menu_states import AdminMenuState
from utils.get_user import admin_only, staff_only
from utils.logging_config import bot_logger


@staff_only
async def admin_menu(call: CallbackQuery, state: FSMContext, role: str):
    """ Отображение клавиатуры админ-панели """
    await state.set_state(AdminMenuState.admin_menu)
    await call.message.edit_text(text='Вы вошли в админ-панель', reply_markup=admin_btn(role=role))


@admin_only
async def admin_menu_handler(call: CallbackQuery, state: FSMContext, role: str):
    """ Вход в админ клавиатуру """
    bot_logger.info('Вход в панель админа')
    await state.set_state(AdminMenuState.admin)
    await call.message.edit_text(text='Меню администратора',
                                 reply_markup=admin_kb())
