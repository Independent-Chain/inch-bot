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
    wallet_storage_path: str
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
            token=env('token'),
            admin_ids=list(map(int, env.list('admin_ids'))),
            ton_api='ton_api',
            wallet_storage_path='wallet_storage_path',
        ),
        db=DatabaseConfig(
            scheme=env('scheme'),
            host=env('host'),
            username=env('username'),
            password=env('password'),
        )
    )
