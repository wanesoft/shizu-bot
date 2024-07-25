import json

from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext

from bot.shizhu import buttons
from bot.shizhu.consts import *
from bot.ai_bot import AiBot
from bot.shizhu.state import DialogStates
from bot.utils.string_utils import generate_hex_string
from storage.storage import s
from storage.entities import *


@AiBot.dp.message(CommandStart())
async def command_start_handler(message: Message, command: CommandObject, state: FSMContext) -> None:
    args = command.args
    await message.answer(f"Your payload: {args}")

    kb = buttons.main_menu()
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="рандомный плейсхолдер"
    )

    await message.answer(HELLO_MESSAGE, parse_mode='HTML', reply_markup=keyboard)

    await state.set_state(DialogStates.main_menu)
    data = await state.get_data()
    if not data:
        ref_id = generate_hex_string()
        await s.create_refinfo_by_ref_id(ref_id, message.chat.id)
        new_user = User.from_message(message, ref_id)
        await state.update_data(user=new_user.model_dump())






        # user = await s.get_refinfo_by_ref_id(ref_id)

        # data = await state.get_data()
        # us = data['user']
        # uu = User.model_validate(us)
        # uu.fullname = "ebalo"
        # await state.update_data(user=uu.model_dump())