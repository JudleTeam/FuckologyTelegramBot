from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc import callbacks

about_blogger = InlineKeyboardMarkup(row_width=1)
about_blogger.add(
    InlineKeyboardButton('Канал «Бьютимаргиналия»', url='t.me/beautymarginalia')
)

about_fuckology = InlineKeyboardMarkup(row_width=1)
about_fuckology.add(
    InlineKeyboardButton('Описание #нахуйлогии', callback_data='file'),
    InlineKeyboardButton('Тариф «встрепенуться»', callback_data=callbacks.rate.new(index=0)),
    InlineKeyboardButton('Тариф «начать действовать»', callback_data=callbacks.rate.new(index=1)),
    InlineKeyboardButton('Тариф «хуярить с Машей»', callback_data=callbacks.rate.new(index=2)),
    InlineKeyboardButton('Написать нам по делу', url='t.me/polinagorbenko')
)

admin_main = InlineKeyboardMarkup(row_width=1)
admin_main.add(
    InlineKeyboardButton('Поменять текст сообщения', callback_data='change_message'),
    InlineKeyboardButton('Изменить цены', callback_data='to_rates_update'),
    InlineKeyboardButton('Вкл/выкл продажи', callback_data='switch_sells'),
    InlineKeyboardButton('Закрыть', callback_data='close')
)

admin_change_message = InlineKeyboardMarkup(row_width=1)
admin_change_message.add(
    InlineKeyboardButton('Про #нахуйлогию', callback_data=callbacks.change_message.new('show', 1)),
    InlineKeyboardButton('Про Машу Милерюс', callback_data=callbacks.change_message.new('show', 2)),
    InlineKeyboardButton('Тариф «встрепенуться»', callback_data=callbacks.change_message.new('show', 3)),
    InlineKeyboardButton('Тариф «начать действовать»', callback_data=callbacks.change_message.new('show', 4)),
    InlineKeyboardButton('Тариф «хуярить с Машей»', callback_data=callbacks.change_message.new('show', 5)),
    InlineKeyboardButton('Продажи закрыты', callback_data=callbacks.change_message.new('show', 'sells_closed_text')),
    InlineKeyboardButton('Назад', callback_data='to_admin')
)

admin_rates = InlineKeyboardMarkup(row_width=1)
admin_rates.add(
    InlineKeyboardButton('Тариф «встрепенуться»', callback_data=callbacks.admin_rate_choose.new(index=0)),
    InlineKeyboardButton('Тариф «начать действовать»', callback_data=callbacks.admin_rate_choose.new(index=1)),
    InlineKeyboardButton('Тариф «хуярить с Машей»', callback_data=callbacks.admin_rate_choose.new(index=2)),
    InlineKeyboardButton('Назад', callback_data='to_admin')
)

after_payment = InlineKeyboardMarkup()
after_payment.add(
    InlineKeyboardButton('Перейти в чат', url='https://t.me/+H9DaC1Ap_cwwZGZi')
)


cancel_price_input = InlineKeyboardMarkup()
cancel_price_input.add(
    InlineKeyboardButton('Отмена', callback_data='cancel')
)


def get_period_choose_keyboard(rate_index):
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton('Первый', callback_data=callbacks.admin_period_choose.new(index=rate_index, period=0)),
        InlineKeyboardButton('Второй', callback_data=callbacks.admin_period_choose.new(index=rate_index, period=1)),
        InlineKeyboardButton('Третий', callback_data=callbacks.admin_period_choose.new(index=rate_index, period=2)),
        InlineKeyboardButton('Финальная цена', callback_data=callbacks.admin_period_choose.new(index=rate_index, period='final')),
        InlineKeyboardButton('Назад', callback_data='to_rates_update'),
    )

    return keyboard


def get_rate_keyboard(rate_price, index):
    keyboard = InlineKeyboardMarkup(row_width=1)

    if rate_price == 0:
        keyboard.add(
            InlineKeyboardButton('Оплатить', callback_data='sell_closed')
        )
    else:
        keyboard.add(
            InlineKeyboardButton('Оплатить', callback_data=callbacks.rate_pay.new(price=rate_price, index=index))
        )

    keyboard.add(
        InlineKeyboardButton('Договор оферты', url='https://telegra.ph/Dogovor-oferta-okazaniya-obrazovatelnyh-uslug-12-03'),
        InlineKeyboardButton('Политика о персональных данных', url='https://telegra.ph/Politika-v-otnoshenii-obrabotki-personalnyh-dannyh-12-07-4'),
        InlineKeyboardButton('Назад', callback_data='to_main')
    )

    return keyboard


def get_change_message_keyboard(id):
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton('Изменить сообщение', callback_data=callbacks.change_message.new('change', str(id))),
        InlineKeyboardButton('Назад', callback_data='change_message')
    )

    return keyboard


def get_cancel_button(id):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton('Отмена', callback_data=callbacks.change_message.new('change_cancel', id))
    )

    return keyboard
