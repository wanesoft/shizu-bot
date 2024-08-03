from aiogram.fsm.state import StatesGroup, State


class DialogStates(StatesGroup):
    waiting_for_alive_photo_pic = State()
    waiting_for_alive_photo_video = State()
    waiting_for_alive_photo_working = State()
    waiting_for_shizu_photo_working = State()
    waiting_for_payment_gens = State()
    waiting_for_payment_sub = State()
    main_menu = State()