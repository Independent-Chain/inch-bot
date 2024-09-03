from aiogram.types import Message, CallbackQuery
from database import t_users


class Translator:
    @staticmethod
    def language(event: Message | CallbackQuery):
        language: str = t_users.select(("language",), "user_id", event.from_user.id)
        return language

    @staticmethod
    def text(event: Message | CallbackQuery, strings: dict, key: str) -> str:
        language: str = t_users.select(("language", ), "user_id", event.from_user.id)
        if language not in ["ru", "en"]:
            language: str = "en"
        return strings[key][language]
