import json
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType, Message

from tgbot.misc import callbacks, messages
from tgbot.keyboards import inline_keyboards


async def show_pay_menu(call: CallbackQuery, callback_data: dict):
    config = call.bot.get('config')

    price = int(callback_data['price'])
    index = int(callback_data['index'])
    title = config.bot.rates[index].title

    product = LabeledPrice(label='Настоящая Машина Времени', amount=5000)

    # increase invoice id
    with open('tgbot/static/messages.json', 'r') as file:
        data = json.load(file)
    invoice_id = data['invoice_id']
    data['invoice_id'] = invoice_id + 1
    with open('tgbot/static/messages.json', 'w') as file:
        json.dump(data, file)

    data = {
      "InvoiceId": 100,
      "Receipt": {
        "sno": "osn",
        "items": [
          {
            "name": "Товар 1",
            "quantity": 1,
            "sum": 50,
            "tax": "vat10",
            "payment_method": "full_payment",
            "payment_object": "commodity"
          }
        ]
      }
    }

    await call.bot.send_invoice(
        call.message.chat.id,
        title='Тест',
        description='Описание',
        provider_token=config.robokassa.token,
        provider_data=data,
        currency='rub',
        prices=[product],
        start_parameter='time-machine-example',
        payload='some-invoice-payload-for-our-internal-use'
    )

    await call.answer()


async def get_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    print(pre_checkout_query.id)
    ans = await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, True)
    print(ans)


async def process_successful_payment(message: Message):
    print('successful_payment:')
    pmnt = message.successful_payment.to_python()
    for key, val in pmnt.items():
        print(f'{key} = {val}')

    await message.answer(messages.after_payment, reply_markup=inline_keyboards.after_payment)


def register_pay(dp: Dispatcher):
    dp.register_callback_query_handler(show_pay_menu, callbacks.rate_pay.filter())
    dp.register_pre_checkout_query_handler(get_pre_checkout_query, lambda query: True)
    dp.register_message_handler(process_successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)
