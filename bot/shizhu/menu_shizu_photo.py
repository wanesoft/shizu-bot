import asyncio

from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram import F

from bot.shizhu import buttons
from bot.shizhu.consts import *
from bot.ai_bot import AiBot
from bot.shizhu.state import DialogStates
from storage.storage import s


@AiBot.dp.message(F.text == BUTTON_ALIVE_SHIZUFACE)
async def command_shizu_photo_handler(message: Message, state: FSMContext) -> None:
    kb = buttons.bottom()
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="рандомный плейсхолдер"
    )

    user = await s.get_user_by_id(message.chat.id)
    user.balance -= 1
    await s.update_user(user)
    await message.answer(ALIVE_SHIZUFACE_WAIT_PIC_MESSAGE, parse_mode='HTML', reply_markup=keyboard)
    await state.set_state(DialogStates.main_menu)