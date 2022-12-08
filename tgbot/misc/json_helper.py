import json


def _get_reg_users() -> list:
    with open('tgbot/static/messages.json', 'r') as file:
        data = json.load(file)
    return data['reg_users']


def is_registered(telegram_id: int) -> bool:
    if telegram_id in _get_reg_users():
        return True
    return False


def get_data() -> dict:
    with open('tgbot/static/messages.json', 'r') as file:
        return json.load(file)


def register_user_json(telegram_id: int):
    data = get_data()
    data['reg_users'].append(telegram_id)
    with open('tgbot/static/messages.json', 'w') as file:
        json.dump(data, file, indent=4)


def register_user(google_sheets, user):
    telegram_id = user.id
    if not is_registered(telegram_id):
        register_user_json(telegram_id)
        google_sheets.register_user(user.mention, user.username, user.full_name)
