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
            "ru": ( f"Добро пожаловать в <b>inch Community</b> 🌟 Мы хотим сделать мир блокчейн-технологий открытым и доступным для всех."
                    f"\n\n"
                    f"Запустите процесс добычи прямо сейчас. В награду вы будете получать поинты <b>$tINCH</b>, который можно будет <u>обменять на наши жетоны</u> в сети <b>TON</b>. Приглашайте друзей и получайте бонус! ☘️ Чем больше друзей - тем больше наше сообщество."
                    f"\n\n"
                    f"Проект полностью Open Source. Это значит, что каждый может сделать свой вклад в развитие <b>Independent Chain</b> 🚀"),
            "en": ( f"Welcome to the <b>inch Community</b> 🌟 We want to make the world of blockchain technology open and accessible to everyone."  
                    f"\n\n"
                    f"Start the mining process right now. In the future, you will receive <b>$tINCH</b> points, which can be <u>exchanged for our jettons</u> in the <b>TON</b> network. Invite friends and receive a community bonus! ☘️ The more friends, the larger our community."
                    f"\n\n"
                    f"Project is completely Open Source. This means that everyone can contribute to the development of <b>Independent Chain</b> 🚀")
            }
    }

    locale = message.from_user.language_code
    photo_url = "https://raw.githubusercontent.com/Independent-Chain/inch-bot/main/src/INCH.png"

    await message.answer_photo(
        photo = photo_url,
        caption = strings["greeting"][language(locale)],
        reply_markup = MainModule.modules["start"].keyboard(language(locale))
    )
