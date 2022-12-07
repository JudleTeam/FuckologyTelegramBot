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
    periods: list[Period]


@dataclass
class Robokassa:
    token: str


@dataclass
class GoogleSheets:
    credentials_file: str
    spreadsheet_id: str



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
    robokassa: Robokassa
    google_sheets: GoogleSheets
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    rates = [
        Rate(
            title='Встрепенуться',
            periods=[
                Period(start=datetime.datetime(2022, 12, 8, 14, 00), end=datetime.datetime(2022, 12, 10, 23, 59), price=5_000),
                Period(start=datetime.datetime(2022, 12, 12, 13, 00), end=datetime.datetime(2022, 12, 13, 23, 59), price=7_000),
                Period(start=datetime.datetime(2022, 12, 13), end=datetime.datetime(2022, 12, 13, 23, 59), price=10_000)
            ]
        ),
        Rate(
            title='Начать действовать',
            periods=[
                Period(start=datetime.datetime(2022, 12, 8, 14, 00), end=datetime.datetime(2022, 12, 10, 23, 59), price=20_000),
                Period(start=datetime.datetime(2022, 12, 12, 13, 00), end=datetime.datetime(2022, 12, 13, 23, 59), price=25_000),
                Period(start=datetime.datetime(2022, 12, 12), end=datetime.datetime(2022, 12, 12), price=30_000)
            ]
        ),
        Rate(
            title='Хуярить с Машей',
            periods=[
                Period(start=datetime.datetime(2022, 12, 8, 14, 00), end=datetime.datetime(2022, 12, 10, 23, 59), price=70_000),
                Period(start=datetime.datetime(2022, 12, 12, 13, 00), end=datetime.datetime(2022, 12, 13, 23, 59), price=80_000),
                Period(start=datetime.datetime(2022, 12, 13), end=datetime.datetime(2022, 12, 13, 23, 59), price=100_000)
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
        robokassa=Robokassa(
            token=env.str('ROBOKASSA_TOKEN')
        ),
        google_sheets=GoogleSheets(
            spreadsheet_id=env.str('SPREADSHEET_ID'),
            credentials_file=env.str('CREDENTIALS_FILE')
        ),
        misc=Miscellaneous()
    )
