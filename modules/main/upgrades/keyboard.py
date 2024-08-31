from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import Translator


def keyboard(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Улучшить реактор", callback_data="upgrade_reactor"),
            InlineKeyboardButton(text="Улучшить хранилище", callback_data="upgrade_storage"),
            InlineKeyboardButton(text="Назад", callback_data="mining"),
        ],
        "en": [
            InlineKeyboardButton(text="Upgrade reactor", callback_data="upgrade_reactor"),
            InlineKeyboardButton(text="Upgrade storage", callback_data="upgrade_storage"),
            InlineKeyboardButton(text="Back", callback_data="mining"),
        ]
    }

    language: str = Translator.language(event)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0])
    builder.row(buttons[language][1])
    builder.row(buttons[language][2])
    return builder.as_markup()