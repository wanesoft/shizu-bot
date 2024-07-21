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

from storage.storage import Storage


TOKEN = getenv("BOT_TOKEN")


class AiBot:

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    storage = Storage()
    dp = Dispatcher(storage=storage.storage)

    def __init__(self):
        print('go')
    
    async def start(self):
        from bot.shizhu.menu_start import (
            command_start_handler,
        )
        from bot.shizhu.menu_home import (
            command_home_handler,
        )
        from bot.shizhu.menu_alive_photo import (
            alive_photo_ask_pic_handler,
            alive_photo_ask_video_handler,
            alive_photo_working,
        )
        from bot.shizhu.menu_balance import (
            command_balance_handler,
        )
        from bot.shizhu.menu_shizu_photo import (
            command_shizu_photo_handler,
        )
        await self.dp.start_polling(self.bot)