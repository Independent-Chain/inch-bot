from aiogram import F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database import t_users
from modules.main import MainModule
from utils import Markdown as md, Translator


def wallet(language: str, address: str) -> str:
    if address == "NULL":
        if language == "ru":
            return "Не привязан"
        if language == "en":
            return "Not linked"
    else:
        return address


@MainModule.router.message(Command("profile"), F.chat.type == ChatType.PRIVATE)
async def h_profile(message: Message, state: FSMContext):

    user = t_users.user(message.from_user.id)

    strings: dict[str, dict] = {
        "profile": {
            "ru": (f"Привет, {md.url(f'{message.from_user.first_name}', f'https://t.me/{message.from_user.username}')} 👋\n"
                   f"{md.bold('Ваш UID')}: {user.uid}\n"
                   f"{md.bold('Баланс')}: {user.balance} $tINCH\n"
                   f"{md.bold('Друзья')}: {user.referals}\n"
                   f"{md.bold('Ton Space')}: {md.monospaced(wallet(user.language, user.wallet))}\n"
                   f"\n"
                   f"{md.bold('Реферальная ссылка')}:\n"
                   f"{md.monospaced(f't.me/inch_coin_bot?start={user.user_id}')}\n"
                   f"(Нажмите, чтобы скопировать)"),
            "en": (f"Hello, {md.url(f'{message.from_user.first_name}', f'https://t.me/{message.from_user.username}')} 👋\n"
                   f"{md.bold('Your UID')}: {user.uid}\n"
                   f"{md.bold('Balance')}: {user.balance} $tINCH\n"
                   f"{md.bold('Friends')}: {user.referals}\n"
                   f"{md.bold('Ton Space')}: {md.monospaced(wallet(user.language, user.wallet))}\n"
                   f"\n"
                   f"{md.bold('Referal link')}:\n"
                   f"{md.monospaced(f't.me/inch_coin_bot?start={user.user_id}')}\n"
                   f"(Click to copy)")
        }
    }

    await state.clear()

    await message.answer(
        text=Translator.text(message, strings, "profile"),
        reply_markup=MainModule.modules["profile"].keyboard(message),
        disable_web_page_preview=True
    )


@MainModule.router.callback_query(F.data == "profile")
async def h_profile(callback: CallbackQuery, state: FSMContext):

    user = t_users.user(callback.from_user.id)

    strings: dict[str, dict] = {
        "profile": {
            "ru": (f"Привет, {md.url(f'{callback.from_user.first_name}', f'https://t.me/{callback.from_user.username}')} 👋\n"
                   f"{md.bold('Ваш UID')}: {user.uid}\n"
                   f"{md.bold('Баланс')}: {user.balance} $tINCH\n"
                   f"{md.bold('Друзья')}: {user.referals}\n"
                   f"{md.bold('Ton Space')}: {md.monospaced(wallet(user.language, user.wallet))}\n"
                   f"\n"
                   f"{md.bold('Реферальная ссылка')}:\n"
                   f"{md.monospaced(f't.me/inch_coin_bot?start={user.user_id}')}\n"
                   f"(Нажмите, чтобы скопировать)"),
            "en": (f"Hello, {md.url(f'{callback.from_user.first_name}', f'https://t.me/{callback.from_user.username}')} 👋\n"
                   f"{md.bold('Your UID')}: {user.uid}\n"
                   f"{md.bold('Balance')}: {user.balance} $tINCH\n"
                   f"{md.bold('Friends')}: {user.referals}\n"
                   f"{md.bold('Ton Space')}: {md.monospaced(wallet(user.language, user.wallet))}\n"
                   f"\n"
                   f"{md.bold('Referal link')}:\n"
                   f"{md.monospaced(f't.me/inch_coin_bot?start={user.user_id}')}\n"
                   f"(Click to copy)")
        }
    }

    await state.clear()
    await callback.answer(show_alert=False)

    try:
        await callback.message.edit_text(
            text=Translator.text(callback, strings, "profile"),
            reply_markup=MainModule.modules["profile"].keyboard(callback),
            disable_web_page_preview=True
        )
    except:
        pass