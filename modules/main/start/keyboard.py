from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def keyboard(locale: str) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Открыть приложение", web_app = WebAppInfo(url="https://inch-app.ru")),
            InlineKeyboardButton(text="Канал проекта", url="https://t.me/inch_ton_cis")

        ],
        "en": [
            InlineKeyboardButton(text="Open webapp", web_app = WebAppInfo(url="https://inch-app.ru")),
            InlineKeyboardButton(text="Project channel", url="https://t.me/inch_ton")
        ]
    }
    
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[locale][0])
    builder.row(buttons[locale][1])
    return builder.as_markup()
