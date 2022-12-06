import json
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards import inline_keyboards
from tgbot.misc import states, callbacks


async def show_messages_to_change_menu(call: CallbackQuery):
    await call.message.edit_text('Сообщения', reply_markup=inline_keyboards.admin_change_message)
    await call.answer()


async def show_change_message_menu(call: CallbackQuery, callback_data: dict):
    message_id = callback_data['id']
    with open('tgbot/static/messages.json', 'r') as file:
        data = json.load(file)
    await call.message.edit_text(data[message_id], reply_markup=inline_keyboards.get_change_message_keyboard(message_id))
    await call.answer()


async def change_message(call: CallbackQuery, callback_data: dict, state: FSMContext):
    message_id = callback_data['id']
    
    await states.MessageChangeState.waiting_for_input.set()
    await state.update_data(id=message_id, menu_message_id=call.message.message_id)
    await call.message.edit_text('Введите новое сообщение', reply_markup=inline_keyboards.get_cancel_button(message_id))
    await call.answer()


async def get_changed_message(message: Message, state: FSMContext):
    new_message = message.text

    async with state.proxy() as data:
        message_id = data['id']
        menu_message_id = data['menu_message_id']
    
    with open('tgbot/static/messages.json', 'r') as file:
        data = json.load(file)
    data[message_id] = new_message
    with open('tgbot/static/messages.json', 'w') as file:
        json.dump(data, file)

    await state.finish()
    await message.delete()
    await message.bot.delete_message(message.from_id, menu_message_id)

    
    await message.answer(data[message_id], reply_markup=inline_keyboards.get_change_message_keyboard(message_id))


async def cancel_change(call: CallbackQuery, callback_data: dict):
    message_id = callback_data['id']
    with open('tgbot/static/messages.json', 'r') as file:
        data = json.load(file)
    await call.message.edit_text(data[message_id], reply_markup=inline_keyboards.get_change_message_keyboard(message_id))
    await call.answer()


async def close_button(call: CallbackQuery):
    await call.message.delete()
    await call.answer()


def register_admin(dp: Dispatcher):
    dp.register_callback_query_handler(show_messages_to_change_menu, text='change_message')
    dp.register_callback_query_handler(show_change_message_menu, callbacks.change_message.filter(type='show'))
    dp.register_callback_query_handler(change_message, callbacks.change_message.filter(type='change'))
    dp.register_message_handler(get_changed_message, state=states.MessageChangeState.waiting_for_input)
    dp.register_callback_query_handler(cancel_change, callbacks.change_message.filter(type='change_cancel'), state='*')
    dp.register_callback_query_handler(close_button, text='close')

