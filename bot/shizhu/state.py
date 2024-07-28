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


class DialogStates(StatesGroup):
    waiting_for_alive_photo_pic = State()
    waiting_for_alive_photo_video = State()
    waiting_for_alive_photo_working = State()
    waiting_for_shizu_photo_working = State()
    main_menu = State()