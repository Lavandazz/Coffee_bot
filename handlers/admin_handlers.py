
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.admin_keyboards import admin_btn, admin_kb

from keyboards.menu_keyboard import inline_menu_kb
from states.menu_states import MenuState, AdminMenuState
from utils.get_user import admin_only, staff_only

from utils.logging_config import bot_logger


@staff_only
async def admin_menu(call: CallbackQuery, state: FSMContext, role: str):
    """ Отображение клавиатуры админ-панели """
    # if role in ["admin", "barista"]:
    await state.set_state(AdminMenuState.admin_menu)
    await call.message.edit_text(text='Вы вошли в админ-панель', reply_markup=admin_btn(role=role))
    # else:
    #     await call.message.answer(text='нет прав')


@admin_only
async def admin_menu_handler(call: CallbackQuery, state: FSMContext, role: str):
    """ Вход в админ клавиатуру """
    bot_logger.info('Вход в панель админа')
    await state.set_state(AdminMenuState.admin)
    # if role == 'admin':
    await call.message.edit_text(text='Вы в меню администратора',
                                 reply_markup=admin_kb())
    # else:
    #     await call.message.edit_text(text='У вас нет прав для этого действия.',
    #                                  reply_markup=await inline_menu_kb(call.from_user.id))
