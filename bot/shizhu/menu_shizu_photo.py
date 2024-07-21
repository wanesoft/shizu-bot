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


@AiBot.dp.message(F.text == BUTTON_ALIVE_SHIZUFACE)
async def command_shizu_photo_handler(message: Message, state: FSMContext) -> None:
    kb = buttons.bottom()
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="рандомный плейсхолдер"
    )

    data = await state.get_data()
    await state.update_data(balance=int(data["balance"]) - 1)
    await message.answer(ALIVE_SHIZUFACE_WAIT_PIC_MESSAGE, parse_mode='HTML', reply_markup=keyboard)
    await state.set_state(DialogStates.main_menu)