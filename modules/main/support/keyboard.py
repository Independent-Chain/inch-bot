from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import Translator


def keyboard(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Поддержка", url="https://t.me/inch_support"),
            InlineKeyboardButton(text="Пользовательское соглашение", url="https://teletype.in/@inch_ton/user_agreement_ru"),
            InlineKeyboardButton(text="Назад", callback_data="profile"),
        ],
        "en": [
            InlineKeyboardButton(text="Support", url="https://t.me/inch_support"),
            InlineKeyboardButton(text="User agreement", url="https://teletype.in/@inch_ton/user_agreement_en"),
            InlineKeyboardButton(text="Back", callback_data="profile"),
        ]
    }

    language: str = Translator.language(event)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0])
    builder.row(buttons[language][1])
    builder.row(buttons[language][2])
    return builder.as_markup()
