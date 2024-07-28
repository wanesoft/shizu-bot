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

    kb = buttons.main_menu()
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="рандомный плейсхолдер"
    )

    await message.answer(HELLO_MESSAGE, parse_mode='HTML', reply_markup=keyboard)

    await state.set_state(DialogStates.main_menu)
    data = await s.get_user_by_id(message.chat.id)
    if not data:
        ref_id = generate_hex_string()
        await s.create_refinfo_by_ref_id(ref_id, message.chat.id)
        new_user = User.from_message(message, ref_id)
        await s.create_user(new_user)
        u = await s.get_user_by_id(new_user.id)
        u.fullname = message.chat.full_name
        await s.update_user(u)

        if args:
            friend_ref_info = await s.get_refinfo_by_ref_id(args)
            if friend_ref_info:
                await AiBot.bot.send_message(friend_ref_info.user_id, "Ваш друг добавился по реферальной ссылке. +2 генерации на баланс")
                friend_user = await s.get_user_by_id(friend_ref_info.user_id)
                friend_user.balance += 2
                await s.update_user(friend_user)





        # u = await s.get_user_by_id(new_user.id)
        # u.fullname = "fsdfsdfdsf"
        # await s.update_user(u)
        # user = await s.get_refinfo_by_ref_id(ref_id)

        # data = await state.get_data()
        # us = data['user']
        # uu = User.model_validate(us)
        # uu.fullname = "ebalo"
        # await state.update_data(user=uu.model_dump())