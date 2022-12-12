import json
import datetime
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType, Message

from tgbot.config import Rate
from tgbot.misc import callbacks, messages, states
from tgbot.keyboards import inline_keyboards, reply_keyboards

from tgbot.misc.json_helper import get_data, register_user


async def show_pay_menu(call: CallbackQuery, callback_data: dict):
    google_sheets = call.bot.get('google_sheets')
    register_user(google_sheets, call.from_user)

    config = call.bot.get('config')

    price = int(callback_data['price'])
    index = int(callback_data['index'])
    title = config.bot.rates[index].title

    title = f'Тариф "{title}"'

    product = LabeledPrice(label=title, amount=price * 100)

    # increase invoice id
    data = get_data()
    invoice_id = data['invoice_id']
    data['invoice_id'] = invoice_id + 1
    with open('tgbot/static/messages.json', 'w') as file:
        json.dump(data, file, indent=4)

    data = {
        "InvoiceId": invoice_id,
        "Receipt": {
            "items": [
                {
                    "name": title,
                    "quantity": 1,
                    "sum": price,
                    "tax": "none",
                    "payment_method": "full_payment",
                    "payment_object": "service"
                }
            ]
        }
    }
    index = index + 3
    #  can't send simple nums due to robokassa
    if index == 3:
        payload = 'one'
    elif index == 4:
        payload = 'two'
    elif index == 5:
        payload = 'three'

    await call.bot.send_invoice(
        call.message.chat.id,
        title=title,
        description='Описание',
        provider_token=config.robokassa.token,
        provider_data=data,
        currency='rub',
        prices=[product],
        start_parameter='beautybot',
        payload=payload
    )

    await call.answer()


async def get_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, True)


async def process_successful_payment(message: Message, state: FSMContext):
    payment = message.successful_payment.to_python()
    payload = payment['invoice_payload']
    if payload == 'one':
        index = 3
    elif payload == 'two':
        index = 4
    elif payload == 'three':
        index = 5
    # test
    # index = 3

    user = message.from_user
    await states.AfterPaymentState.waiting_for_phone.set()
    await state.update_data(index=index, username=user.username, full_name=user.full_name, mention=user.mention)
    await message.answer('Пожалуйста, оставьте ваш номер телефона: ', reply_markup=reply_keyboards.cancel)


async def show_final_menu(message: Message, state: FSMContext):
    phone = message.text.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
    if not phone.isdigit() or not (10 <= len(phone) <= 12):
        await message.answer('Неверный номер телефона, попробуйте ещё раз')
        return

    config = message.bot.get('config')
    # get order id
    json_data = get_data()
    invoice_id = json_data['invoice_id']

    async with state.proxy() as data:
        index = data['index']
        username = data['username']
        full_name = data['full_name']
        mention = data['mention']

    title = config.bot.rates[index - 3].title
    title = f'Тариф {title}'
    await message.answer(messages.first, reply_markup=reply_keyboards.main_menu)
    await message.answer(messages.after_payment, reply_markup=inline_keyboards.after_payment)
    await state.finish()
    # get price
    rate: Rate = config.bot.rates[index - 3]
    for ind, period in enumerate(rate.periods):
        if period.start <= datetime.datetime.now() <= period.end:
            price = json_data['rates'][index - 3]['prices'][ind]
            break
    else:
        price = json_data['rates'][index - 3]['final_price']

    google_sheets = message.bot.get('google_sheets')
    google_sheets.add_customer(title, mention, invoice_id, datetime.datetime.now() + datetime.timedelta(hours=3), price,
                               phone, username, full_name)


def register_pay(dp: Dispatcher):
    dp.register_callback_query_handler(show_pay_menu, callbacks.rate_pay.filter())
    dp.register_pre_checkout_query_handler(get_pre_checkout_query, lambda query: True)
    dp.register_message_handler(process_successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)
    # dp.register_message_handler(process_successful_payment, commands=['test'], state='*')
    dp.register_message_handler(show_final_menu, state=states.AfterPaymentState.waiting_for_phone)
