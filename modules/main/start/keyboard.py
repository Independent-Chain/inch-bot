from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def language(language_code: str) -> str:
    if language_code not in ["ru", "en"]:
        return "en"
    else:
        return language_code


def keyboard(locale: str) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Открыть приложение", web_app = WebAppInfo(url="https://inch-app.ru")),
            InlineKeyboardButton(text="Канал проекта", url="https://t.me/inch_ton")

        ],
        "en": [
            InlineKeyboardButton(text="Open webapp", web_app = WebAppInfo(url="https://inch-app.ru")),
            InlineKeyboardButton(text="Project channel", url="https://t.me/inch_ton")
        ]
    }
    
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language(locale)][0])
    builder.row(buttons[language(locale)][1])
    return builder.as_markup()
