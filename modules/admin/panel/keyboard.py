from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import Translator


def keyboard(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Статистика", callback_data="statistics"),
            InlineKeyboardButton(text="Рассылка", callback_data="mailing"),
            InlineKeyboardButton(text="Изменить константы", callback_data="constants"),
            InlineKeyboardButton(text="Сгенерировать промокоды", callback_data="generate_codes"),
            InlineKeyboardButton(text="Получить промокоды", callback_data="get_codes"),
            InlineKeyboardButton(text="Закрыть панель управления", callback_data="close_panel"),
        ],
        "en": [
            InlineKeyboardButton(text="Statistics", callback_data="statistics"),
            InlineKeyboardButton(text="Mailing", callback_data="mailing"),
            InlineKeyboardButton(text="Change constants", callback_data="constants"),
            InlineKeyboardButton(text="Generate promo codes", callback_data="generate_codes"),
            InlineKeyboardButton(text="Get promo codes", callback_data="get_codes"),
            InlineKeyboardButton(text="Close control panel", callback_data="close_panel"),
        ]
    }

    language: str = Translator.language(event)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0])
    builder.row(buttons[language][1])
    builder.row(buttons[language][2])
    builder.row(buttons[language][3])
    builder.row(buttons[language][4])
    builder.row(buttons[language][5])
    return builder.as_markup()