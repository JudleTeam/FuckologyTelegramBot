from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
main_menu.add(
    KeyboardButton('Про #нахуйлогию'),
    KeyboardButton('Про Машу Милерюс')
)

cancel_button = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_button.add(
    KeyboardButton('')
)
