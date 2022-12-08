import json
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.handlers.main import show_admin
from tgbot.keyboards import inline_keyboards
from tgbot.misc import states, callbacks
from tgbot.misc.json_helper import get_data


async def show_messages_to_change_menu(call: CallbackQuery):
    await call.message.edit_text('Сообщения', reply_markup=inline_keyboards.admin_change_message)
    await call.answer()


async def show_change_message_menu(call: CallbackQuery, callback_data: dict):
    message_id = callback_data['id']
    with open(r'tgbot/static/messages.json', 'r') as file:
        data = json.load(file)
    await call.message.edit_text(data[message_id], reply_markup=inline_keyboards.get_change_message_keyboard(message_id))
    await call.answer()


async def change_message(call: CallbackQuery, callback_data: dict, state: FSMContext):
    message_id = callback_data['id']
    
    await states.MessageChangeState.waiting_for_input.set()
    await state.update_data(id=message_id, menu_message_id=call.message.message_id)
    await call.message.edit_text('Введите новое сообщение', reply_markup=inline_keyboards.get_cancel_button(message_id))
    await call.answer()


async def switch_sells(call: CallbackQuery):
    data = get_data()

    data['open_sells'] = not data['open_sells']
    with open(r'tgbot/static/messages.json', 'w') as file:
        json.dump(data, file, indent=4)

    await call.answer('Успешно!', show_alert=True)
    await show_admin(call)


async def get_changed_message(message: Message, state: FSMContext):
    new_message = message.text

    async with state.proxy() as data:
        message_id = data['id']
        menu_message_id = data['menu_message_id']
    
    with open(r'tgbot/static/messages.json', 'r') as file:
        data = json.load(file)
    data[message_id] = new_message
    with open(r'tgbot/static/messages.json', 'w') as file:
        json.dump(data, file, indent=4)

    await message.delete()
    await message.bot.delete_message(message.from_id, menu_message_id)

    await message.answer(data[message_id], reply_markup=inline_keyboards.get_change_message_keyboard(message_id))
    await state.finish()


async def cancel_change(call: CallbackQuery, callback_data: dict, state: FSMContext):
    message_id = callback_data['id']
    with open(r'tgbot/static/messages.json', 'r') as file:
        data = json.load(file)
    await call.message.edit_text(data[message_id], reply_markup=inline_keyboards.get_change_message_keyboard(message_id))
    await call.answer()
    await state.finish()


async def show_rates(call: CallbackQuery):
    await call.message.edit_text('Выберите тариф', reply_markup=inline_keyboards.admin_rates)


async def show_periods(call: CallbackQuery, callback_data: dict):
    config = call.bot.get('config')

    index = int(callback_data['index'])
    await call.message.edit_text(f'Тариф "{config.bot.rates[index].title}"\nВыберите период',
                                 reply_markup=inline_keyboards.get_period_choose_keyboard(index))
    await call.answer()


async def start_price_input(call: CallbackQuery, callback_data: dict, state: FSMContext):
    period = callback_data['period']
    rate_index = int(callback_data['index'])
    config = call.bot.get('config')

    with open(r'tgbot/static/messages.json', 'r') as file:
        data = json.load(file)

    if period.isdigit():
        price = data['rates'][rate_index]['prices'][int(period)]
        period_str = int(period) + 1
    else:
        price = data['rates'][rate_index]['final_price']
        period_str = 'финальный'

    await call.message.edit_text(f'Тариф "{config.bot.rates[rate_index].title}"\nПериод {period_str}\nТекущая цена: {price}\nВведите новую цену:',
                                 reply_markup=inline_keyboards.cancel_price_input)
    await states.PriceUpdateState.waiting_for_price.set()
    await state.update_data(rate_index=rate_index, period=period)
    await call.answer()


async def get_new_price(message: Message, state: FSMContext):
    new_price = message.text
    if not new_price.isdigit():
        await message.answer('Неверный формат цены, попробуйте ещё раз', reply_markup=inline_keyboards.cancel_price_input)
        return

    new_price = int(new_price)
    with open(r'tgbot/static/messages.json', 'r') as file:
        json_data = json.load(file)

    async with state.proxy() as data:
        if data['period'].isdigit():
            json_data['rates'][int(data['rate_index'])]['prices'][int(data['period'])] = new_price
        else:
            json_data['rates'][int(data['rate_index'])]['final_price'] = new_price

    with open(r'tgbot/static/messages.json', 'w') as file:
        json.dump(json_data, file, indent=4)

    await message.answer('Успешно!')
    await message.answer('Админ меню', reply_markup=inline_keyboards.admin_main)
    await state.finish()


async def cancel_price_input(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('Админ меню', reply_markup=inline_keyboards.admin_main)
    await state.finish()


async def close_button(call: CallbackQuery):
    await call.message.delete()
    await call.answer()


def register_admin(dp: Dispatcher):
    dp.register_callback_query_handler(show_messages_to_change_menu, text='change_message')
    dp.register_callback_query_handler(show_change_message_menu, callbacks.change_message.filter(type='show'))
    dp.register_callback_query_handler(show_rates, text='to_rates_update')
    dp.register_callback_query_handler(show_periods, callbacks.admin_rate_choose.filter())
    dp.register_callback_query_handler(start_price_input, callbacks.admin_period_choose.filter())
    dp.register_message_handler(get_new_price, state=states.PriceUpdateState.waiting_for_price)
    dp.register_callback_query_handler(cancel_price_input, text='cancel', state=states.PriceUpdateState.waiting_for_price)
    dp.register_callback_query_handler(change_message, callbacks.change_message.filter(type='change'))
    dp.register_message_handler(get_changed_message, state=states.MessageChangeState.waiting_for_input)
    dp.register_callback_query_handler(cancel_change, callbacks.change_message.filter(type='change_cancel'), state='*')
    dp.register_callback_query_handler(close_button, text='close')
    dp.register_callback_query_handler(switch_sells, text='switch_sells')
