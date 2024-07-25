from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram import F

from bot.shizhu import buttons
from bot.shizhu.consts import *
from bot.ai_bot import AiBot
from bot.shizhu.state import DialogStates
from storage.entities import *
from storage.storage import s

@AiBot.dp.message(F.text == BUTTON_BALANCE)
async def command_balance_handler(message: Message, state: FSMContext) -> None:
    kb = buttons.pay_wall()
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="рандомный плейсхолдер"
    )

    data = await state.get_data()
    user = User.model_validate(data["user"])
    await message.answer(f"Доступно генераций: {user.balance}", parse_mode='HTML', reply_markup=keyboard)

    ref_info = await s.get_refinfo_by_ref_id(user.ref_id)
    ref_info.balance_from_link += 1
    await s.update_refinfo_by_ref_id(user.ref_id, ref_info)

    await message.answer(f"Баланс за рефералку увеличен на: {ref_info.balance_from_link}", parse_mode='HTML', reply_markup=keyboard)

    await state.set_state(DialogStates.main_menu)