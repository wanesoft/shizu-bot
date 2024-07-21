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


@AiBot.dp.message(F.text == BUTTON_HOME)
async def command_home_handler(message: Message, state: FSMContext) -> None:
    kb = buttons.main_menu()
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="рандомный плейсхолдер"
    )

    await message.answer(HELLO_MESSAGE, parse_mode='HTML', reply_markup=keyboard)
    await state.set_state(DialogStates.main_menu)