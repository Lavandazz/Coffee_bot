from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.models_db import User
from keyboards.admin_keyboards import admin_rights, yes_or_no_btn, all_baristas_or_admins_kb
from keyboards.back_keyboard import back_button
from states.menu_states import AdminMenuState, BaristaRegistrationState
from utils.get_user import admin_only
from utils.logging_config import bot_logger


@admin_only
async def barista_rights(call: CallbackQuery, state: FSMContext, role: str):
    """Отправление клавиатуры для регистрации или удаления прав бариста/админа"""
    await call.message.edit_text(
        text='Выберите действие',
        reply_markup=admin_rights())
    await state.set_state(AdminMenuState.rights)


@admin_only
async def start_register_name_barista(call: CallbackQuery, state: FSMContext, role: str):
    """
    Регистрация бариста.
    :param call:
    :param state:
    :param role: admin
    """
    print(call.data)
    await call.message.edit_text(
        text='Введите имя пользователя telegram`.`\n'
             'Для точности данных *необходимо зайти в профиль пользователя и нажать "Имя пользователя"*`.`\n'
             'Имя с *@* копируется автоматически`.`',
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=back_button()
    )
    await state.set_state(BaristaRegistrationState.registration_name)


@admin_only
async def enter_role_barista(message: Message, state: FSMContext, role: str):
    """Ожидание регистрации"""
    name = message.text.replace('@', '')
    await state.update_data(name_barista=name)
    bot_logger.info(f'сохранение в память name_barista {name}')
    user = await User.get_or_none(username=name)

    if user:
        await message.answer(
            text=f'Вы уверены, что хотите добавить роль бариста для {user.username}?',
            reply_markup=yes_or_no_btn()
        )
        bot_logger.info(f'Изменение роли для  {user.username} на роль barista')
        await state.set_state(BaristaRegistrationState.save_name)
    else:
        await message.answer("Пользователь с таким ником не найден. Попробуйте ещё раз.")
        # прописать отмену, если нажата кнопка back



@admin_only
async def save_barista_role(call: CallbackQuery, state: FSMContext, role: str):
    """Сохранение роли бариста"""
    data = await state.get_data()
    name_barista = data.get('name_barista')
    bot_logger.debug(f'Сохранение бариста data.get(name_barista) {name_barista}')

    try:
        user = await User.get_or_none(username=name_barista)
        bot_logger.info(f'Сохранение роли бариста для {user.username}')
        if not user:
            await call.message.edit_text("Ошибка: пользователь не найден.")
            await state.clear()
            return

        if call.data == "yes":
            user.role = "barista"
            await user.save()
            await call.message.edit_text(
                f"✅ Пользователь {user.username} теперь бариста!",
                reply_markup=admin_rights()
            )
            bot_logger.debug(f"Пользователь {user.username} получил роль barista")

        elif call.data == "no":
            await call.message.edit_text(text="❌ Операция отменена.",
                                         reply_markup=admin_rights())

    except Exception as e:
        bot_logger.error(f"Ошибка во время добавления бариста: {e}")
        await call.message.edit_text("⚠️ Произошла ошибка. Попробуйте снова.")

    await state.set_state(AdminMenuState.rights)


@admin_only
async def baristas_for_delete(call: CallbackQuery, state: FSMContext, role: str):
    """
    Показывает кнопки с именами, кому необходимо присвоить роль юзера.
    :param call: Удалить бариста
    :param state: delete_name
    :param role: admin
    """
    try:
        all_baristas = await User.filter(role='barista').all()
        bot_logger.debug(f'Получение списка барист для удаления {all_baristas}')
        if all_baristas:
            await call.message.edit_text(
                text='Выберите бариста, которому необходимо присвоить роль пользователя.',
                reply_markup=await all_baristas_or_admins_kb(all_baristas, 'delete')
            )
        else:
            await call.message.edit_text(
                text='Никого нет для удаления.',
                reply_markup=await all_baristas_or_admins_kb(all_baristas)
            )
        await state.set_state(BaristaRegistrationState.delete_name)
    except Exception as e:
        bot_logger.error(f'Ошибка удаления бариста {e}')


@admin_only
async def delete_barista(call: CallbackQuery, state: FSMContext, role: str):
    """
    Удаление бариста из списка и присваивание ему роли юзера.
    Для смены роли получаем User.id из CallbackQuery = delete_{user.id}
    :param call: delete_{user.id}
    """
    call_for_delete = call.data.split('_')[1]  # получаем id
    try:
        user = await User.get_or_none(id=call_for_delete)
        user.role = "user"
        await user.save()
        admin_call = call.from_user.id
        bot_logger.debug(f'{admin_call} Изменил роль бариста {user.username} на роль {user}')
        await call.answer(text=f'Роль для {user.username} изменена')
    except Exception as e:
        bot_logger.error(f'Ошибка удаления бариста {e}')

