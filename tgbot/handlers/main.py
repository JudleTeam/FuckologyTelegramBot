import datetime
import json

from aiogram import Dispatcher
from aiogram.types import CallbackQuery, InputFile

from tgbot.config import Rate
from tgbot.keyboards import inline_keyboards
from tgbot.misc import messages, callbacks
from tgbot.misc.json_helper import register_user


async def send_file(call: CallbackQuery):
    doc = InputFile(r'tgbot/static/description.pdf')
    await call.message.answer_document(doc)
    await call.answer()


async def show_main_menu(call: CallbackQuery):
    await call.message.edit_text(messages.about_fuckology, reply_markup=inline_keyboards.about_fuckology)


async def show_sell_closed(call: CallbackQuery):
    await call.answer('Продажи закрыты!', show_alert=True)


async def show_rate(call: CallbackQuery, callback_data: dict):
    google_sheets = call.bot.get('google_sheets')
    register_user(google_sheets, call.from_user)
    config = call.bot.get('config')
    index = int(callback_data['index'])
    rate: Rate = config.bot.rates[index]

    with open('tgbot/static/messages.json', 'r') as file:
        data = json.load(file)

    for ind, period in enumerate(rate.periods):
        if period.start <= datetime.datetime.now() <= period.end:
            price = data['rates'][index]['prices'][ind]
            price_str = f'{price} руб.'
            break
        else:
            if datetime.datetime.now() < period.start:
                price = 0
                price_str = f'Следующее окно продаж откроется {period.start.day} декабря в {period.start.hour}.{"00" if str(period.start.minute) == "0" else period.start.minute}'
                break
    else:
        price = data['rates'][index]['final_price']
        price_str = f'{price} руб. финальная'

    await call.message.edit_text(
        messages.rate.format(
            description=data[str(index + 3)],
            price=price_str
        ),
        reply_markup=inline_keyboards.get_rate_keyboard(price, index)
    )
    await call.answer()


async def show_admin(call: CallbackQuery):
    google_sheets = call.bot.get('google_sheets')
    register_user(google_sheets, call.from_user)
    await call.message.edit_text('Админ меню', reply_markup=inline_keyboards.admin_main) 


def register_main(dp: Dispatcher):
    dp.register_callback_query_handler(send_file, text='file')
    dp.register_callback_query_handler(show_main_menu, text='to_main')
    dp.register_callback_query_handler(show_sell_closed, text='sell_closed')
    dp.register_callback_query_handler(show_rate, callbacks.rate.filter())
    dp.register_callback_query_handler(show_admin, text='to_admin')
