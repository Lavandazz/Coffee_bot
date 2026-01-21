from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.models_db import User
from keyboards.admin_keyboards import all_baristas_or_admins_kb, yes_or_no_btn, admin_rights
from keyboards.back_keyboard import back_button
from states.menu_states import AdminRegistrationState, AdminMenuState
from helpers.get_user import admin_only
from config.logging_config import bot_logger


@admin_only
async def show_baristas_to_admin(call: CallbackQuery, state: FSMContext, role: str):
    """
    Отображение всех бариста как клавиатура для простого выбора админа.
    Для того, чтобы повысить роль юзера до админа, сначала необходимо юзера повысить до бариста, затем до админа.
    """
    all_baristas = await User.filter(role='barista').all()
    if all_baristas:
        await call.message.edit_text(text='Кого назначить админом?',
                                     reply_markup=await all_baristas_or_admins_kb(all_baristas, 'barista'))
    if not all_baristas:
        await call.message.edit_text(text='Сначала необходимо дать права бариста',
                                     reply_markup=back_button())
    await state.set_state(AdminRegistrationState.search_name)


@admin_only
async def approve_admin(call: CallbackQuery, state: FSMContext, role: str):
    """
    Отправление клавиатуры для подтверждения роли админа.
    Сохранение user_id в state для дальнейшего изменения роли пользователя.
    Отправляется клавиатура для подтверждения изменения роли "Да/нет"
    """
    if call.data == 'back':
        await call.message.edit_text(text='Возврат в управление правами', reply_markup=admin_rights())
        await state.set_state(AdminMenuState.rights)
        return
    user_id = call.data.split('_')[1]
    await state.update_data(id=user_id)
    user = await User.get_or_none(id=user_id)

    await call.message.edit_text(
        text=f'Вы уверены, что хотите добавить роль админа для {user.username}?',
        reply_markup=yes_or_no_btn())
    await state.set_state(AdminRegistrationState.waiting_choice)


@admin_only
async def save_role_admin(call: CallbackQuery, state: FSMContext, role: str):
    """
    Сохранение роли админа
    """
    data = await state.get_data()
    id_user = data['id']
    if call.data == "yes":
        try:
            await User.filter(id=id_user).update(role=role)
            bot_logger.info(f'смена роли админа для')
            await call.message.edit_text(text='Сохранено', reply_markup=admin_rights()
            )

        except Exception as e:
            await call.message.edit_text(text=f'что-то пошло не так {e}')

    elif call.data == "no":
        await state.clear()
        await call.message.edit_text(text="❌ Операция отменена.",
                                     reply_markup=admin_rights())

    await state.set_state(AdminRegistrationState.save_name)


@admin_only
async def show_admins_for_delete(call: CallbackQuery, state: FSMContext, role: str):
    """
    Отображение всех авдминов как клавиатура

    """
    admins = await User.filter(role='admin').all()
    await call.message.edit_text(
        text='Выберите админа для смены прав',
        reply_markup=await all_baristas_or_admins_kb(admins, 'delete')
    )
    bot_logger.debug('отправлена клавиатура для выбора админа на удаление')

    await state.set_state(AdminRegistrationState.delete_name)


@admin_only
async def delete_admin(call: CallbackQuery, state: FSMContext, role: str):
    """
    Удаление админа из списка и присваивание ему роли юзера.
    Для смены роли получаем User.id из CallbackQuery = delete_{user.id}
    :param call: delete_{user.id}
    """
    bot_logger.debug('функция удаления админа')
    call_for_delete = call.data.split('_')[1]  # получаем id
    try:
        user = await User.get_or_none(id=call_for_delete)
        user.role = "user"
        await user.save()
        admin_call = call.from_user.id
        bot_logger.debug(f'{admin_call} Изменил роль админа {user.username} на роль {user}')
        await call.message.edit_text(text=f'Роль для {user.username} изменена', reply_markup=admin_rights())
        await state.set_state(AdminRegistrationState.save_name)
    except Exception as e:
        bot_logger.error(f'Ошибка изменения роли админа {e}')
