from aiogram import Dispatcher
from aiogram.types import CallbackQuery, LabeledPrice

from tgbot.misc import callbacks


async def show_pay_menu(call: CallbackQuery, callback_data: dict):
    config = call.bot.get('config')
    price = callback_data['price']

    product = LabeledPrice(label='Настоящая Машина Времени', amount=4200000)
    print(config.robokassa.token)
    await call.bot.send_invoice(
        call.message.chat.id,
        title='Тест',
        description='Описание',
        provider_token=config.robokassa.token,
        currency='rub',
        prices=[product],
        start_parameter='time-machine-example',
        payload='some-invoice-payload-for-our-internal-use'
    )
    # await call.answer('Функционал пока недоступен!', show_alert=True)
    await call.answer()


def register_pay(dp: Dispatcher):
    dp.register_callback_query_handler(show_pay_menu, callbacks.rate_pay.filter())
