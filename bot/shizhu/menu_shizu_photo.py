import asyncio

from aiogram.types import Message, ReplyKeyboardMarkup, input_file
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import F

from bot.shizhu import buttons
from bot.shizhu.consts import *
from bot.ai_bot import AiBot
from bot.shizhu.state import DialogStates
from storage.storage import s


SHIZU_PHOTO_GEN_PRICE = 1

async def emulate_request_to_father(chat_id, file):
    print(chat_id)
    await asyncio.sleep(15)
    file = input_file.FSInputFile(file)
    await AiBot.bot.send_photo(chat_id=chat_id, photo=file, caption=ALIVE_PHOTO_DONE)


@AiBot.dp.message(F.text == BUTTON_ALIVE_SHIZUFACE)
async def command_shizu_photo_handler(message: Message, state: FSMContext) -> None:
    kb = buttons.bottom()
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="рандомный плейсхолдер"
    )

    await message.answer(ALIVE_SHIZUFACE_WAIT_PIC_MESSAGE, parse_mode='HTML', reply_markup=keyboard)    
    await state.set_state(DialogStates.waiting_for_shizu_photo_working)


@AiBot.dp.message(StateFilter(DialogStates.waiting_for_shizu_photo_working))
async def alive_photo_ask_video_handler(message: Message, state: FSMContext):
    kb = buttons.bottom()
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder=ALIVE_PHOTO_WAIT_VIDEO_MESSAGE
    )

    if message.photo:
        await message.answer(ALIVE_SHIZU_WORKING, parse_mode='HTML', reply_markup=keyboard)
        
        user = await s.get_user_by_id(message.chat.id)
        user.balance -= SHIZU_PHOTO_GEN_PRICE
        await s.update_user(user)
        
        photo = message.photo[-1]
        file_info = await AiBot.bot.get_file(photo.file_id)
        downloaded_file = await AiBot.bot.download_file(file_info.file_path)
        with open(f"{photo.file_unique_id}.jpg", "wb") as f:
            f.write(downloaded_file.read())
        await state.set_state(DialogStates.waiting_for_alive_photo_video)
        await emulate_request_to_father(message.chat.id, f"{photo.file_unique_id}.jpg")
    else:
        await message.answer(ALIVE_PHOTO_WAIT_PIC_MESSAGE_RETRY, parse_mode='HTML', reply_markup=keyboard)