from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import Translator


def invite(event: Message | CallbackQuery) -> str:
    user_id: int = event.from_user.id
    language: str = Translator.language(event)

    text: dict[str, str] = {
        "ru": f"\nПрисоединяйся к Independent Chain.\nНам важен каждый ⚡️\nhttps://t.me/inch_coin_bot?start={user_id}",
        "en": f"\nJoin the Independent Chain.\nEveryone is important to us ⚡️\nhttps://t.me/inch_coin_bot?start={user_id}"
    }

    return text[language]


def keyboard(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="💳 Кошелёк", callback_data="wallet"),
            InlineKeyboardButton(text="🔥 Добыча", callback_data="mining"),
            InlineKeyboardButton(text="♻️ Промокоды", callback_data="codes"),
            InlineKeyboardButton(text="🎉 События", callback_data="events"),
            InlineKeyboardButton(text="🛟 Поддержка", callback_data="support"),
            InlineKeyboardButton(text="Пригласить друга", switch_inline_query=invite(event))
        ],
        "en": [
            InlineKeyboardButton(text="💳 Wallet", callback_data="wallet"),
            InlineKeyboardButton(text="🔥 Mining", callback_data="mining"),
            InlineKeyboardButton(text="♻️ Codes", callback_data="codes"),
            InlineKeyboardButton(text="🎉 Events", callback_data="events"),
            InlineKeyboardButton(text="🛟 Support", callback_data="support"),
            InlineKeyboardButton(text="Invite friend", switch_inline_query=invite(event))
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