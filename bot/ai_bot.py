from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram import F

from storage.storage import Storage
from bot.shizhu import payment


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
            command_payment_gens,
        )
        from bot.shizhu.menu_shizu_photo import (
            command_shizu_photo_handler,
        )
        self.dp.message.register(payment.send_invoice_handler, Command(commands="donate"))
        self.dp.pre_checkout_query.register(payment.pre_checkout_handler)
        self.dp.message.register(payment.success_payment_handler, F.successful_payment)
        self.dp.message.register(payment.pay_support_handler, Command(commands="paysupport"))
        await self.dp.start_polling(self.bot)