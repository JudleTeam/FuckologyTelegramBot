from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from tgbot.misc import callbacks


async def show_pay_menu(call: CallbackQuery):
    await call.answer('Функционал пока недоступен!', show_alert=True)


def register_pay(dp: Dispatcher):
    dp.register_callback_query_handler(show_pay_menu, callbacks.rate_pay.filter())
