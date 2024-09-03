import asyncio
import datetime

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import t_users, t_mining


class StorageChecker:
    strings: dict[str, dict] = {
        "notification": {
            "ru": ("Хранилище заполнено 🔥\n"
                   "Время собирать добычу."),
            "en": ("Storage is full 🔥\n"
                   "It's time to collect the loot.")
        }
    }
    storage: list[int] = []

    @classmethod
    async def check_storage(cls, bot: Bot):
        m_users: list = t_mining.select(())
        for u in m_users:
            user = t_users.user(userid=u[0])
            m_user = t_mining.user(userid=u[0])

            # Check storage.
            time_difference: float = (datetime.datetime.now() - m_user.last_claim).total_seconds()
            if time_difference > m_user.storage * 3600:
                if user.user_id not in cls.storage:
                    cls.storage.append(user.user_id)
                    try:
                        await bot.send_message(
                            chat_id=user.user_id,
                            text=cls.strings["notification"][user.language],
                            reply_markup=cls.keyboard_builder(user.language),
                        )
                    except TelegramForbiddenError:
                        pass
            else:
                try:
                    cls.storage.remove(user.user_id)
                except ValueError:
                    pass

        await asyncio.sleep(60)
        await cls.check_storage()

    @classmethod
    def keyboard_builder(cls, language: str) -> InlineKeyboardMarkup:
        buttons: dict[str, list] = {
            "ru": [
                InlineKeyboardButton(text="Собрать добычу", callback_data="mining")
            ],
            "en": [
                InlineKeyboardButton(text="Claim loot", callback_data="mining")
            ]
        }

        builder = InlineKeyboardBuilder()
        builder.row(buttons[language][0])
        return builder.as_markup()
