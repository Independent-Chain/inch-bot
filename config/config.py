from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    scheme: str
    host: str
    username: str
    password: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    ton_api: str


@dataclass
class Config:
    secrets: TgBot
    db: DatabaseConfig


def load_config() -> Config:

    env: Env = Env()
    env.read_env()

    return Config(
        secrets=TgBot(
            token=env('API_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        ),
        db=DatabaseConfig(
            database=env('DATABASE'),
            db_host=env('DB_HOST'),
            db_user=env('DB_USER'),
            db_password=env('DB_PASSWORD')
        )
    )
