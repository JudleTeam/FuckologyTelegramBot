from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
main_menu.add(
    KeyboardButton('Про #нахуйлогию'),
    KeyboardButton('Про Машу Милерюс')
)

get_phone = ReplyKeyboardMarkup(resize_keyboard=True)
get_phone.add(
    KeyboardButton('Отправить номер', request_contact=True)
)

cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add(
    KeyboardButton('Отмена')
)
