from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database import t_users
from modules.group import GroupModule
from utils import Markdown as md


def format_text(user) -> str:
    leaders: list = t_users.order(("username", "balance"), "balance", 10)

    text: str = f"{md.bold('Таблица лидеров')}:\n"
    for i in range(len(leaders)):
        index = i + 1
        text += f"{index}. @{leaders[i][0]} - {leaders[i][1]} $tINCH\n"

    text += f"\n{t_users.rating(user.user_id)}. @{user.username} - {user.balance} $tINCH"
    return text


@GroupModule.router.message(Command("leaderboard"))
async def leaderboard_(message: Message, state: FSMContext) -> None:

    user = t_users.user(message.from_user.id)
    text: str = format_text(user)

    if message.chat.type == "private":
        await message.answer(text=text)
    elif F.chat.type == "supergroup":
        await message.reply(text=text)
    return None