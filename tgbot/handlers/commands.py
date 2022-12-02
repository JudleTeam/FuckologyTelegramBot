from aiogram import Dispatcher
from aiogram.types import Message, InputFile

from tgbot.keyboards import reply_keyboards, inline_keyboards
from tgbot.misc import messages


async def command_start(message: Message):
    await message.answer(messages.first, reply_markup=reply_keyboards.main_menu)


async def send_about_blogger(message: Message):
    await message.answer(messages.about_blogger, reply_markup=inline_keyboards.about_blogger)


async def send_about_fuckology(message: Message):
    await message.answer(messages.about_fuckology, reply_markup=inline_keyboards.about_fuckology)


def register_commands(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'], state='*')
    dp.register_message_handler(send_about_blogger, text='Про Машу Милерюс')
    dp.register_message_handler(send_about_fuckology, text='Про #нахуйлогию')

