import json

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards import reply_keyboards, inline_keyboards
from tgbot.misc import messages


async def command_start(message: Message):
    await message.answer(messages.first, reply_markup=reply_keyboards.main_menu)


async def send_about_blogger(message: Message):
    with open(r'tgbot/static/messages.json', 'r') as file:
        data = json.load(file)

    await message.answer(data['2'], reply_markup=inline_keyboards.about_blogger)


async def send_about_fuckology(message: Message):
    with open(r'tgbot/static/messages.json', 'r') as file:
        data = json.load(file)

    await message.answer(data['1'], reply_markup=inline_keyboards.about_fuckology)


async def command_admin(message: Message):
    await message.delete()
    await message.answer('Админ меню', reply_markup=inline_keyboards.admin_main)


async def cancel_state(message: Message, state: FSMContext):
    await message.answer(messages.first, reply_markup=reply_keyboards.main_menu)
    await state.finish()


def register_commands(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'], state='*')
    dp.register_message_handler(command_admin, commands=['admin'], state='*', is_admin=True)
    dp.register_message_handler(send_about_blogger, text='Про Машу Милерюс')
    dp.register_message_handler(send_about_fuckology, text='Про #нахуйлогию')
    dp.register_message_handler(cancel_state, text='Отмена', state='*')
