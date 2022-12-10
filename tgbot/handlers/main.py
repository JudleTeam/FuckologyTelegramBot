import datetime
import json

from aiogram import Dispatcher
from aiogram.types import CallbackQuery, InputFile

from tgbot.config import Rate
from tgbot.keyboards import inline_keyboards
from tgbot.misc import messages, callbacks
from tgbot.misc.json_helper import register_user, get_data
from tgbot.misc.json_helper import get_data


async def send_file(call: CallbackQuery):
    doc = InputFile(r'tgbot/static/description.pdf')
    await call.message.answer_document(doc)
    await call.answer()


async def show_main_menu(call: CallbackQuery):
    await call.message.edit_text(messages.about_fuckology, reply_markup=inline_keyboards.about_fuckology)


async def show_sell_closed(call: CallbackQuery):
    data = get_data()
    
    await call.answer(data['sells_closed_text'], show_alert=True)


async def show_rate(call: CallbackQuery, callback_data: dict):
    google_sheets = call.bot.get('google_sheets')
    register_user(google_sheets, call.from_user)
    config = call.bot.get('config')
    index = int(callback_data['index'])
    rate: Rate = config.bot.rates[index]
    data = get_data()

    if not data['open_sells']:
        price = 0
        price_str = data['sells_closed_text']
    else:
        for ind, period in enumerate(rate.periods):
            if period.start <= datetime.datetime.now() + datetime.timedelta(hours=3) <= period.end:  # fix timezone
                price = data['rates'][index]['prices'][ind]
                price_str = f'{price} руб.'
                break
            else:
                if datetime.datetime.now() + datetime.timedelta(hours=3) < period.start:
                    price = 0
                    price_str = (f'Следующее окно продаж откроется {period.start.day} декабря в '
                                 f'{period.start.hour}.{"00" if str(period.start.minute) == "0" else period.start.minute}')
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
    data = get_data()
    if data['open_sells']:
        sells_status = 'Открыты'
    else:
        sells_status = 'Закрыты'

    await call.message.edit_text(f'Админ меню\nПродажи: {sells_status}', reply_markup=inline_keyboards.admin_main)


def register_main(dp: Dispatcher):
    dp.register_callback_query_handler(send_file, text='file')
    dp.register_callback_query_handler(show_main_menu, text='to_main')
    dp.register_callback_query_handler(show_sell_closed, text='sell_closed')
    dp.register_callback_query_handler(show_rate, callbacks.rate.filter())
    dp.register_callback_query_handler(show_admin, text='to_admin')
