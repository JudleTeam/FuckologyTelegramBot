import datetime

from aiogram import Dispatcher
from aiogram.types import CallbackQuery, InputFile

from tgbot.config import Rate
from tgbot.keyboards import inline_keyboards
from tgbot.misc import messages, callbacks


async def send_file(call: CallbackQuery):
    doc = InputFile(r'tgbot/static/description.pdf')
    await call.message.answer_document(doc)
    await call.answer()


async def show_main_menu(call: CallbackQuery):
    await call.message.edit_text(messages.about_fuckology, reply_markup=inline_keyboards.about_fuckology)


async def show_sell_closed(call: CallbackQuery):
    await call.answer('Продажи закрыты!', show_alert=True)


async def show_rate(call: CallbackQuery, callback_data: dict):
    config = call.bot.get('config')
    rate: Rate = config.bot.rates[int(callback_data['index'])]

    for period in rate.periods:
        if period.start <= datetime.datetime.now() <= period.end:
            price = period.price
            price_str = f'{price} руб.'
            break
    else:
        price = 0
        price_str = 'Продажи закрыты'

    await call.message.edit_text(
        messages.rate.format(
            description=rate.description,
            price=price_str
        ),
        reply_markup=inline_keyboards.get_rate_keyboard(price)
    )
    await call.answer()


def register_main(dp: Dispatcher):
    dp.register_callback_query_handler(send_file, text='file')
    dp.register_callback_query_handler(show_main_menu, text='to_main')
    dp.register_callback_query_handler(show_sell_closed, text='sell_closed')
    dp.register_callback_query_handler(show_rate, callbacks.rate.filter())
