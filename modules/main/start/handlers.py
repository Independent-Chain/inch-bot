from aiogram import F
from aiogram.enums import ChatType, ChatMemberStatus
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.config import bot
from modules.main import MainModule

from utils.translator import language


@MainModule.router.message(F.chat.type == ChatType.PRIVATE, Command("start"))
async def h_start(message: Message, state: FSMContext) -> None:

    strings: dict[str, dict] = {
        "greeting": {
            "ru": (f"текст"),
            "en": (f"text")
            }
    }

    locale = message.from_user.language_code
    url = "https://rgo.ru/upload/content_block/images/9ca8302358b777e143cd6e314058266b/7065323d0aa2e3fa6e8764c4f57f1655.jpg?itok=sawvdjq3"
    
    await message.answer_photo(
        photo = url,
        caption = strings["greeting"][language(locale)],
        reply_markup = MainModule.modules["start"].keyboard(locale)
    )
