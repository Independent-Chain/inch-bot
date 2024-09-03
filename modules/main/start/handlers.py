import datetime

from aiogram import F, Bot
from aiogram.enums import ChatType, ChatMemberStatus
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database import t_users
from modules.main import MainModule
from utils import Markdown as md, Translator


async def check_subscribe(user_id: int, bot) -> bool:
    status = await bot.get_chat_member(chat_id="@inch_ton", user_id=user_id)
    if status.status != ChatMemberStatus.LEFT:
        return True
    else:
        return False


def language(language_code: str) -> str:
    if language_code not in ["ru", "en"]:
        return "en"
    else:
        return language_code


def inviter(message: Message) -> int | None:
    text: list = message.text.split(" ")
    if len(text) == 2:
        inviter_id: int = int(text[1])
        return inviter_id
    else:
        return None


@MainModule.router.message(F.chat.type == ChatType.PRIVATE, Command("start"))
async def h_start(message: Message, state: FSMContext, bot: Bot) -> None:

    strings: dict[str, dict] = {
        "greeting": {
            "ru": (
                f"Добро пожаловать в {md.bold('Independent Chain')} - крипто-проект, запущенный группой энтузиастов.\n"
                f"\n"
                f"Наша цель - запустить собственную, независимую от коммерческих организаций, спонсоров и сторонних "
                f"организаций блокчейн-сеть с внутресетевой монетой.\n"
                f"\n"
                f"Уже запущена рекламная компания на платформе Telegram в рамках которой было отчеканено 10,000,000 "
                f"жетонов $INCH в сети TON 🔥\n"
                f"\n"
                f"За каждого приглашённого друга вы получите {t_users.referal} $tINCH - внутрення валюта бота. В дальнейшем каждый "
                f"сможет конвертировать свои накопления в жетон $INCH 🔄\n"
                f"\n"
                f"Для просмотра профиля воспользуйтесь командой /profile.\n"
                f"\n"
                f"{md.monospaced('Перед использованием бота настоятельно рекомендуем ознакомиться с пользовательским соглашением.')}"),
            "en": (
                f"Welcome to {md.bold('Independent Chain')}, a crypto project launched by a group of enthusiasts.\n"
                f"\n"
                f"Our goal is to launch our own blockchain network with an intra-network coin, independent of commercial "
                f"organizations, sponsors and third-party organizations.\n"
                f"\n"
                f"An advertising campaign has already been launched on the Telegram platform, within the framework of which 10,000,000 "
                f"$INCH tokens were minted on the TON network🔥\n"
                f"\n"
                f"For each invited friend, you will receive {t_users.referal} $tINCH - the internal currency of the bot. In the future, everyone "
                f"will be able to convert his savings into a $INCH token 🔄\n"
                f"\n"
                f"To view the profile, use the /profile command.\n"
                f"{md.monospaced('Before using the bot, we strongly recommend that you read the user agreement.')}")
        },
        "subscribe": {
            "ru": "Подпишитесь на канал проекта для использования бота.",
            "en": "Subscribe to the project channel to use the bot."
        }
    }

    await state.clear()

    # Check user existence in bot database.
    user = t_users.user(message.from_user.id)
    if user is None:
        t_users.insert(
            user_id=message.from_user.id,
            username=message.from_user.username,
            language=language(message.from_user.language_code),
            wallet="NULL",
            balance=t_users.start,
            referals=0,
            last_code=(datetime.datetime.now() - datetime.timedelta(days=1)),
        )

    inviter_id: int | None = inviter(message)
    if inviter_id is not None:
        if user is None:
            t_users.increase("referals", 1, "user_id", inviter_id)
            t_users.increase("balance", t_users.referal, "user_id", inviter_id)

    if not await check_subscribe(message.from_user.id, bot):
        await message.answer(
            text=Translator.text(message, strings, "subscribe"),
            reply_markup=MainModule.modules["start"].keyboard_subscribe(message)
        )
    else:
        await message.answer(
            text=Translator.text(message, strings, "greeting"),
            reply_markup=MainModule.modules["start"].keyboard(message)
        )


@MainModule.router.callback_query(F.data == "check_subscribe")
async def h_subscribe(callback: CallbackQuery, bot: Bot) -> None:

    strings: dict[str, dict] = {
        "success": {
            "ru": ("Подписка подтверждена ✅\n"
                   "Воспользуйтесь командой → /start"),
            "en": ("Subscription is confirmed ✅\n"
                   "Use command → /start")
        },
        "fail": {
            "ru": "Вы не подписаны на канал 🚫",
            "en": "You are not subscribed to the channel 🚫"
        }
    }

    if await check_subscribe(callback.from_user.id, bot):
        await callback.message.edit_text(
            text=Translator.text(callback, strings, "success")
        )
    else:
        await callback.answer(
            text=Translator.text(callback, strings, "fail"),
            show_alert=True
        )
