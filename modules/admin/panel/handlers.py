from aiogram import F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from modules.admin import AdminModule
from utils import Translator
from config.config import Config, load_config


@AdminModule.router.message(Command("admin"))
async def h_admin(message: Message, state: FSMContext) -> None:

    config: Config = load_config()

    if message.from_user.id not in config.secrets.admin_ids:
        strings: dict[str, dict] = {
            "failed": {
                "ru": "Недостаточно прав для использования данной команды.",
                "en": "There are not enough permissions to use this command."
            }
        }

        await message.answer(
            text=Translator.text(message, strings, "failed")
        )

        return None

    strings: dict[str, dict] = {
        "panel": {
            "ru": f"Добро пожаловать в панель управления Independent Chain Bot, {message.from_user.first_name}.",
            "en": f"Welcome to the Independent Chain Bot control panel, {message.from_user.first_name}."
        }
    }

    await state.clear()

    await message.answer(
        text=Translator.text(message, strings, "panel"),
        reply_markup=AdminModule.modules["panel"].keyboard(message)
    )


@AdminModule.router.callback_query(F.data == "panel")
async def h_admin(callback: CallbackQuery, state: FSMContext) -> None:

    strings: dict[str, dict] = {
        "panel": {
            "ru": f"Добро пожаловать в панель управления Independent Chain Bot, {callback.from_user.first_name}.",
            "en": f"Welcome to the Independent Chain Bot control panel, {callback.from_user.first_name}."
        }
    }

    await state.clear()
    await callback.answer(show_alert=False)

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "panel"),
        reply_markup=AdminModule.modules["panel"].keyboard(callback)
    )


@AdminModule.router.callback_query(F.data == "close_panel")
async def h_admin(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:

    await state.clear()
    await callback.answer(show_alert=False)

    await bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id
    )
