from aiogram import F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database import t_users
from database.table import Admin
from modules.admin import AdminModule
from states import AdminStates
from utils import Markdown as md, Translator


@AdminModule.router.callback_query(F.data == "mailing")
async def h_mailing(callback: CallbackQuery, state: FSMContext) -> None:

    strings: dict[str, dict] = {
        "mailing": {
            "ru": (f"{md.bold('Шаблон для создания рассылки')}:\n"
                   f"\n"
                   f"{md.monospaced('RU text # EN text # RU button title # EN button title # RU link # EN link')}"),
            "en": (f"{md.bold('Template for creating a mailing list')}:\n"
                   f"\n"
                   f"{md.monospaced('RU text # EN text # RU button title # EN button title # RU link # EN link')}"),
        }
    }

    await callback.answer(show_alert=False)
    await state.set_state(AdminStates.mailing)

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "mailing"),
        reply_markup=AdminModule.modules["mailing"].keyboard(callback)
    )


@AdminModule.router.message(StateFilter(AdminStates.mailing))
async def h_mailing_template(message: Message, bot: Bot) -> None:

    strings: dict[str, dict] = {
        "notify": {
            "ru": "Рассылка запущена.",
            "en": "Mailing started."
        }
    }

    await message.answer(
        text=Translator.text(message, strings, "notify")
    )

    template: list = message.text.split("#")
    ru: dict = {
        "text": template[0],
        "button": template[2],
        "link": template[4],
    }
    en: dict = {
        "text": template[1],
        "button": template[3],
        "link": template[5],
    }

    users: list = Admin.ids()

    result: dict = {
        "total": 0,
        "success": 0,
        "fail": 0,
    }

    for user in users:
        language: str = t_users.select(("language",), "user_id", user)
        try:
            result["total"] += 1
            if eval(language)["button"] == "None" and eval(language)["link"] == "None":
                await bot.send_message(
                    chat_id=user,
                    text=eval(language)["text"]
                )
            else:
                await bot.send_message(
                    chat_id=user,
                    text=eval(language)["text"],
                    reply_markup=AdminModule.modules["mailing"].keyboard_constructor(eval(language)["button"], eval(language)["link"])
                )
        except:
            result["fail"] += 1
        else:
            result["success"] += 1

    strings: dict[str, dict] = {
        "result": {
            "ru": (f"{md.bold('Рассылка отправлена')}.\n"
                   f"{md.bold('Всего пользователей')}: {result['total']}\n"
                   f"{md.bold('Успешно отправлено')}: {result['success']}\n"
                   f"{md.bold('Не отправлено')}: {result['fail']}\n"),
            "en": (f"{md.bold('Mailing sent')}.\n"
                   f"{md.bold('Total users')}: {result['total']}\n"
                   f"{md.bold('Successfully sent')}: {result['success']}\n"
                   f"{md.bold('Not sent')}: {result['fail']}\n")
        }
    }

    await message.answer(
        text=Translator.text(message, strings, "result"),
        reply_markup=AdminModule.modules["mailing"].keyboard(message)
    )