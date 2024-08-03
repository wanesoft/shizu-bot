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

    user = await s.get_user_by_id(message.chat.id)
    await message.answer(f"Доступно генераций: {user.balance}", parse_mode='HTML', reply_markup=keyboard)

    ref_info = await s.get_refinfo_by_ref_id(user.ref_id)
    ref_info.balance_from_link += 1
    await s.update_refinfo_by_ref_id(user.ref_id, ref_info)

    await message.answer(f"Баланс за рефералку увеличен на: {ref_info.balance_from_link}", parse_mode='HTML', reply_markup=keyboard)

    await state.set_state(DialogStates.main_menu)


@AiBot.dp.message(F.text == BUTTON_BUY_GENS)
async def command_payment_gens(message: Message, state: FSMContext) -> None:
    kb = buttons.pay_wall_gens()
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="рандомный плейсхолдер"
    )

    await message.answer(BALANCE_PAYMENT_GENS, parse_mode='HTML', reply_markup=keyboard)
    await state.set_state(DialogStates.waiting_for_payment_gens)

@AiBot.dp.message(F.text == BUTTON_PAYMEN_50_GENS)
@AiBot.dp.message(F.text == BUTTON_PAYMEN_100_GENS)
@AiBot.dp.message(F.text == BUTTON_PAYMEN_250_GENS)
@AiBot.dp.message(F.text == BUTTON_PAYMEN_500_GENS)
async def command_payment_gens(message: Message, state: FSMContext) -> None:
    kb = buttons.pay_wall_gens()
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="рандомный плейсхолдер"
    )

    await message.answer(BALANCE_PAYMENT_GENS, parse_mode='HTML', reply_markup=keyboard)
    await state.set_state(DialogStates.waiting_for_payment_gens)
