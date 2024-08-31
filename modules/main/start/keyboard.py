from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import Translator


def keyboard(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Канал проекта", url="https://t.me/inch_ton"),
            InlineKeyboardButton(text="Чат проекта", url="https://t.me/inch_ton_chat"),
            InlineKeyboardButton(text="Пользовательское соглашение", url="https://teletype.in/@inch_ton/user_agreement_ru")
        ],
        "en": [
            InlineKeyboardButton(text="Project channel", url="https://t.me/inch_ton"),
            InlineKeyboardButton(text="Project chat", url="https://t.me/inch_ton_chat"),
            InlineKeyboardButton(text="User agreement", url="https://teletype.in/@inch_ton/user_agreement_en")
        ]
    }

    language: str = Translator.language(event)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0])
    builder.row(buttons[language][1])
    builder.row(buttons[language][2])
    return builder.as_markup()


def keyboard_subscribe(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Канал проекта", url="https://t.me/inch_ton"),
            InlineKeyboardButton(text="Проверить подписку", callback_data="check_subscribe")
        ],
        "en": [
            InlineKeyboardButton(text="Project channel", url="https://t.me/inch_ton"),
            InlineKeyboardButton(text="Check subscribe", callback_data="check_subscribe")
        ]
    }

    language: str = Translator.language(event)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0])
    builder.row(buttons[language][1])
    return builder.as_markup()