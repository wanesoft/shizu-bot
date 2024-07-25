from aiogram.types import KeyboardButton
from bot.shizhu.consts import *

def main_menu():
    return [
        [KeyboardButton(text=BUTTON_ALIVE_PHOTO), KeyboardButton(text=BUTTON_ALIVE_SHIZUFACE)],
        [KeyboardButton(text=BUTTON_REFERRAL), KeyboardButton(text=BUTTON_BALANCE)],
        [KeyboardButton(text=BUTTON_HELP)],
    ]

def bottom():
    return [
        [KeyboardButton(text=BUTTON_HOME)],
    ]

def pay_wall():
    return [
        [KeyboardButton(text=BUTTON_BUY_GENS), KeyboardButton(text=BUTTON_BUY_SUBS)],
        [KeyboardButton(text=BUTTON_REFERRAL), KeyboardButton(text=BUTTON_EARN_GENS)],
        [KeyboardButton(text=BUTTON_HOME)],
    ]
