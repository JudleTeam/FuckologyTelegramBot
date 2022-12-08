from aiogram.dispatcher.filters.state import StatesGroup, State


class MessageChangeState(StatesGroup):
    waiting_for_input = State()


class AfterPaymentState(StatesGroup):
    waiting_for_phone = State()


class PriceUpdateState(StatesGroup):
    waiting_for_price = State()
