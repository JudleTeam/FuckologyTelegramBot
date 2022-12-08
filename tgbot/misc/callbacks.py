from aiogram.utils.callback_data import CallbackData

rate_pay = CallbackData('rate_pay', 'price', 'index')
rate = CallbackData('rate', 'index')
change_message = CallbackData('change_message', 'type', 'id')
admin_rate_choose = CallbackData('adm_rate', 'index')
admin_period_choose = CallbackData('adm_period', 'index', 'period')
