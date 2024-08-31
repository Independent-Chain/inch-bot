from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from modules.main import MainModule
from utils import Translator


def wallet(language: str, address: str) -> str:
    if address == "NULL":
        if language == "ru":
            return "Не привязан"
        if language == "en":
            return "Not linked"
    else:
        return address


@MainModule.router.callback_query(F.data == "support")
async def h_support(callback: CallbackQuery, state: FSMContext):

    strings: dict[str, dict] = {
        "support": {
            "ru": (f"В случае возникновения ошибок или каких-либо проблем с ботом просим написать вас в поддержку.\n"
                   f"\n"
                   f"Опишите проблему и приложите дополнительные материалы (фото, видео) для скорейшего решения вашей проблемы.\n"
                   f"\n"
                   f"В нашем проекте открыта программа баг-хаутинга, которая подробно описана в пользовательском соглашении."),
            "en": (f"In case of errors or any problems with the bot, please write to support.\n"
                   f"\n"
                   f"Describe the problem and attach additional materials (photos, videos) to solve your problem as soon as possible.\n"
                   f"\n"
                   f"A bug-hunting program has been opened in our project, which is described in detail in the user agreement.")
        }
    }

    await callback.answer(show_alert=False)

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "support"),
        reply_markup=MainModule.modules["support"].keyboard(callback)
    )