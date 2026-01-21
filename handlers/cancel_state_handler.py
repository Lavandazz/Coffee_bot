import asyncio
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.menu_keyboard import inline_menu_kb
from config.logging_config import bot_logger


async def cancel_handler(message: Message, bot: Bot, state: FSMContext):
    """ Сброс состояния ввода данных """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    bot_logger.info(f"Состояние ожидания: {current_state} - отменено")
    await asyncio.sleep(0.3)
    await message.answer(f"Действие отменено.\n"
                         f"Возврат в меню",
                         reply_markup=await inline_menu_kb(message.from_user.id))
    # await bot.send_message(message.from_user.id, 'Возврат в меню',
    #                        reply_markup=inline_menu_kb())


async def cancel_state_handler(user_id: int, bot: Bot, state: FSMContext):
    """ Автоматический сброс состояния """
    try:
        current_state = await state.get_state()
        if not current_state:
            # Если состояния нет, ничего не делаем
            return
        await asyncio.sleep(300)
        new_current_state = await state.get_state()
        if current_state == new_current_state:
            # user_id = user_id
            await bot.send_message(user_id, 'Ожидание ввода превышено. Отмена сохранения данных.',
                                   reply_markup=await inline_menu_kb(user_id))
            await state.clear()
            bot_logger.info(f'Состояние сброшено: {current_state} ')

    except Exception as e:
        bot_logger.warning(f"Ошибка в cancel_state_handler: {e}")
