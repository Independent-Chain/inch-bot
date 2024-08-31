from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import Translator


def keyboard(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Назад", callback_data="panel")
        ],
        "en": [
            InlineKeyboardButton(text="Back", callback_data="panel")
        ]
    }

    language: str = Translator.language(event)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0])
    return builder.as_markup()


def keyboard_constructor(text: str, link: str) -> InlineKeyboardMarkup:
    button = InlineKeyboardButton(text=text, url=link)

    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(button)
    return builder.as_markup()