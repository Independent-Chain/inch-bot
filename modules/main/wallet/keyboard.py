from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import Translator


def keyboard(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="TonSpace", callback_data="tonspace"),
            InlineKeyboardButton(text="TonKeeper", callback_data="tonkeeper"),
            InlineKeyboardButton(text="MyTonWallet", callback_data="mytonwallet"),
            InlineKeyboardButton(text="Назад", callback_data="profile"),
        ],
        "en": [
            InlineKeyboardButton(text="TonSpace", callback_data="tonspace"),
            InlineKeyboardButton(text="TonKeeper", callback_data="tonkeeper"),
            InlineKeyboardButton(text="MyTonWallet", callback_data="mytonwallet"),
            InlineKeyboardButton(text="Back", callback_data="profile"),
        ]
    }

    language: str = Translator.language(event)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0])
    builder.row(buttons[language][1])
    builder.row(buttons[language][2])
    builder.row(buttons[language][3])
    return builder.as_markup()


def keyboard_linked(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Поддержка", url="https://t.me/diominvd"),
            InlineKeyboardButton(text="Назад", callback_data="profile"),
        ],
        "en": [
            InlineKeyboardButton(text="Support", url="https://t.me/diominvd"),
            InlineKeyboardButton(text="Back", callback_data="profile"),
        ]
    }

    language: str = Translator.language(event)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0])
    builder.row(buttons[language][1])
    return builder.as_markup()


def keyboard_connect_tonspace(event: Message | CallbackQuery, url: str) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Подключить TonSpace", url=url),
            InlineKeyboardButton(text="Назад", callback_data="profile"),
        ],
        "en": [
            InlineKeyboardButton(text="Connect TonSpace", url=url),
            InlineKeyboardButton(text="Back", callback_data="profile"),
        ]
    }

    language: str = Translator.language(event)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0])
    builder.row(buttons[language][1])
    return builder.as_markup()


def keyboard_connect_tonkeeper(event: Message | CallbackQuery, url: str) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Подключить Tonkeeper", url=url),
            InlineKeyboardButton(text="Назад", callback_data="wallet"),
        ],
        "en": [
            InlineKeyboardButton(text="Connect Tonkeeper", url=url),
            InlineKeyboardButton(text="Back", callback_data="wallet"),
        ]
    }

    language: str = Translator.language(event)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0])
    builder.row(buttons[language][1])
    return builder.as_markup()


def keyboard_connect_mytonwallet(event: Message | CallbackQuery, url: str) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Подключить MyTonWallet", url=url),
            InlineKeyboardButton(text="Назад", callback_data="wallet"),
        ],
        "en": [
            InlineKeyboardButton(text="Connect MyTonWallet", url=url),
            InlineKeyboardButton(text="Back", callback_data="wallet"),
        ]
    }

    language: str = Translator.language(event)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0])
    builder.row(buttons[language][1])
    return builder.as_markup()


def keyboard_connected(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Закрыть", callback_data="profile"),
        ],
        "en": [
            InlineKeyboardButton(text="Close", callback_data="profile"),
        ]
    }

    language: str = Translator.language(event)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0])
    return builder.as_markup()


def keyboard_connected_error(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Поддержка", url="https://t.me/diominvd"),
            InlineKeyboardButton(text="Закрыть", callback_data="profile"),
        ],
        "en": [
            InlineKeyboardButton(text="Support", url="https://t.me/diominvd"),
            InlineKeyboardButton(text="Close", callback_data="profile"),
        ]
    }

    language: str = Translator.language(event)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0])
    builder.row(buttons[language][1])
    return builder.as_markup()
