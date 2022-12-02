import datetime
from dataclasses import dataclass

from environs import Env


@dataclass
class DatabaseConfig:
    host: str
    password: str
    user: str
    database: str
    port: int


@dataclass
class Period:
    start: datetime.datetime
    end: datetime.datetime
    price: int


@dataclass
class Rate:
    title: str
    description: str
    periods: list[Period]


@dataclass
class TelegramBot:
    token: str
    admin_ids: list[int]
    use_redis: bool
    rates: list[Rate]


@dataclass
class Miscellaneous:
    other_params: str = ''


@dataclass
class Config:
    bot: TelegramBot
    database: DatabaseConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    rates = [
        Rate(
            title='Встрепенуться',
            description='Доступ к вебинару (1,5 часа вебинар и полчаса сессия вопрос-ответ) и к материалам.',
            periods=[
                Period(start=datetime.datetime(2022, 12, 5), end=datetime.datetime(2022, 12, 7, 23, 59), price=5_000),
                Period(start=datetime.datetime(2022, 12, 9), end=datetime.datetime(2022, 12, 10, 23, 59), price=7_000),
                Period(start=datetime.datetime(2022, 12, 12), end=datetime.datetime(2022, 12, 12, 23, 59), price=10_000)
            ]
        ),
        Rate(
            title='Начать действовать',
            description=('Доступ к вебинару, материалам и мастер-майндам в малых группах, где мы будем намечать план '
                         'действий вместе с Машей. А также доступ к чатам малых групп, где еще 2 месяца мы будем на '
                         'связи и поддерживать друг друга.'),
            periods=[
                Period(start=datetime.datetime(2022, 12, 5), end=datetime.datetime(2022, 12, 7), price=20_000),
                Period(start=datetime.datetime(2022, 12, 9), end=datetime.datetime(2022, 12, 10), price=25_000),
                Period(start=datetime.datetime(2022, 12, 12), end=datetime.datetime(2022, 12, 12), price=30_000)
            ]
        ),
        Rate(
            title='Хуярить с Машей',
            description=('Доступ к вебинару, материалам и личная работа с Машей в течение 2-х месяцев. Общение в чате, '
                         '4 индивидуальных сессии-звонка с Машей.'),
            periods=[
                Period(start=datetime.datetime(2022, 12, 5), end=datetime.datetime(2022, 12, 7), price=70_000),
                Period(start=datetime.datetime(2022, 12, 9), end=datetime.datetime(2022, 12, 10), price=80_000),
                Period(start=datetime.datetime(2022, 12, 12), end=datetime.datetime(2022, 12, 12), price=100_000)
            ]
        )
    ]

    return Config(
        bot=TelegramBot(
            token=env.str('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMINS'))),
            use_redis=env.bool('USE_REDIS'),
            rates=rates
        ),
        database=DatabaseConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME'),
            port=env.int('DB_PORT')
        ),
        misc=Miscellaneous()
    )
