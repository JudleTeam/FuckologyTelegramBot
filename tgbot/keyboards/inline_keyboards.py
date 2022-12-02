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


def get_rate_keyboard(rate_price):
    keyboard = InlineKeyboardMarkup(row_width=1)

    if rate_price == 0:
        keyboard.add(
            InlineKeyboardButton('Оплатить', callback_data='sell_closed')
        )
    else:
        keyboard.add(
            InlineKeyboardButton('Оплатить', callback_data=callbacks.rate_pay.new(price=rate_price))
        )

    keyboard.add(
        InlineKeyboardButton('Договор оферты', url='telegra.ph'),
        InlineKeyboardButton('Политика о персональных данных', url='telegra.ph'),
        InlineKeyboardButton('Назад', callback_data='to_main')
    )

    return keyboard
