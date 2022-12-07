import json
import datetime
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType, Message

from tgbot.misc import callbacks, messages, states
from tgbot.keyboards import inline_keyboards


async def show_pay_menu(call: CallbackQuery, callback_data: dict):
    config = call.bot.get('config')

    price = int(callback_data['price'])
    index = int(callback_data['index'])
    title = config.bot.rates[index].title

    title = f'Тариф "{title}"'

    product = LabeledPrice(label=title, amount=price * 100)

    # increase invoice id
    with open('tgbot/static/messages.json', 'r') as file:
        data = json.load(file)
    invoice_id = data['invoice_id']
    data['invoice_id'] = invoice_id + 1
    with open('tgbot/static/messages.json', 'w') as file:
        json.dump(data, file)

    data = {
        "InvoiceId": invoice_id,
        "Receipt": {
            "sno": "osn",
            "items": [
                {
                    "name": title,
                    "quantity": 1,
                    "sum": price,
                    "tax": "vat10",
                    "payment_method": "full_payment",
                    "payment_object": "commodity"
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
    pmnt = message.successful_payment.to_python()
    payload = pmnt['invoice_payload']
    if payload == 'one':
        index = 3
    elif payload == 'two':
        index = 4
    elif payload == 'three':
        index = 5

    # await message.answer(messages.after_payment, reply_markup=inline_keyboards.after_payment)
    user = message.from_user
    await states.AfterPaymentState.waiting_for_phone.set()
    await state.update_data(index=index, username=user.username, full_name=user.full_name, mention=user.mention)
    await message.answer('Пожалуйста оставьте ваш номер телефона', reply_markup=inline_keyboards.get_phone)


async def show_final_menu(message: Message, state: FSMContext):
    config = call.bot.get('config')

    phone = message.contact.phone_number
    # get order id
    with open('tgbot/static/messages.json', 'r') as file:
        data = json.load(file)
    invoice_id = data['invoice_id']

    async with state.proxy() as data:
        index = data['index']
        username = data['username']
        full_name = data['full_name']
        mention = data['mention']
    await state.finish()
    title = config.bot.rates[index].title
    # get price
    for period in rate.periods:
        if period.start <= datetime.datetime.now() <= period.end:
            price = period.price
            break

    google_sheets = message.bot.get('google_sheets')
    google_sheets.add_customer(title, mention, invoice_id, datetime.datetime.now(), price, phone, username, full_name)


def register_pay(dp: Dispatcher):
    dp.register_callback_query_handler(show_pay_menu, callbacks.rate_pay.filter())
    dp.register_pre_checkout_query_handler(get_pre_checkout_query, lambda query: True)
    dp.register_message_handler(process_successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)
    dp.register_message_handler(show_final_menu, state=states.AfterPaymentState.waiting_for_phone)
