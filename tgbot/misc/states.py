from aiogram.dispatcher.filters.state import StatesGroup, State


class MessageChangeState(StatesGroup):
    waiting_for_input = State()

