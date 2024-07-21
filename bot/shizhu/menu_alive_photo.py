import asyncio
import logging
import sys
import asyncio
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardButton, input_file
from aiogram.fsm.storage.mongo import MongoStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
import motor.motor_asyncio

from bot.shizhu import buttons
from bot.shizhu.consts import *
from bot.ai_bot import AiBot
from bot.shizhu.state import DialogStates
from bot.utils.string_utils import generate_hex_string


async def emulate_request_to_father(chat_id, file):
    print(chat_id)
    await asyncio.sleep(15)
    file = input_file.FSInputFile(file)
    await AiBot.bot.send_video(chat_id=chat_id, video=file, caption=ALIVE_PHOTO_DONE)


@AiBot.dp.message(F.text == BUTTON_ALIVE_PHOTO)
async def alive_photo_ask_pic_handler(message: Message, state: FSMContext) -> None:
    kb = buttons.bottom()
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder=ALIVE_PHOTO_WAIT_PIC_MESSAGE
    )

    await message.answer(ALIVE_PHOTO_WAIT_PIC_MESSAGE, parse_mode='HTML', reply_markup=keyboard)
    # await message.send_copy(chat_id=message.chat.id)
    await state.set_state(DialogStates.waiting_for_alive_photo_pic)


@AiBot.dp.message(StateFilter(DialogStates.waiting_for_alive_photo_pic))
async def alive_photo_ask_video_handler(message: Message, state: FSMContext):
    kb = buttons.bottom()
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder=ALIVE_PHOTO_WAIT_VIDEO_MESSAGE
    )

    if message.photo:
        await message.answer(ALIVE_PHOTO_WAIT_VIDEO_MESSAGE, parse_mode='HTML', reply_markup=keyboard)
        photo = message.photo[-1]
        file_info = await AiBot.bot.get_file(photo.file_id)
        downloaded_file = await AiBot.bot.download_file(file_info.file_path)
        with open(f"{photo.file_unique_id}.jpg", "wb") as f:
            f.write(downloaded_file.read())
        await state.set_state(DialogStates.waiting_for_alive_photo_video)
    else:
        await message.answer(ALIVE_PHOTO_WAIT_PIC_MESSAGE_RETRY, parse_mode='HTML', reply_markup=keyboard)


@AiBot.dp.message(StateFilter(DialogStates.waiting_for_alive_photo_video))  
async def alive_photo_working(message: Message, state: FSMContext):
    kb = buttons.bottom()
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder=ALIVE_PHOTO_WORKING
    )
    
    if message.video:
        await message.answer(ALIVE_PHOTO_WORKING, parse_mode='HTML', reply_markup=keyboard)
        data = await state.get_data()
        data["balance"] = data["balance"] - 1 
        video = message.video
        file_info = await AiBot.bot.get_file(video.file_id)
        downloaded_file = await AiBot.bot.download_file(file_info.file_path)
        with open(f"{video.file_unique_id}.mp4", "wb") as f:
            f.write(downloaded_file.read())
        await state.set_state(DialogStates.waiting_for_alive_photo_working)
        await emulate_request_to_father(message.chat.id, f"{video.file_unique_id}.mp4")
    else:
        await message.answer(ALIVE_PHOTO_WAIT_VIDEO_MESSAGE_RETRY, parse_mode='HTML', reply_markup=keyboard)