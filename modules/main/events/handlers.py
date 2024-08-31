from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from modules.main import MainModule
from utils import Translator


@MainModule.router.callback_query(F.data == "events")
async def h_events(callback: CallbackQuery, state: FSMContext):

    strings: dict[str, dict] = {
        "events": {
            "ru": "Нет доступных событий",
            "en": "There are no events available"
        }
    }

    await callback.answer(
        text=Translator.text(callback, strings, "events"),
        show_alert=False
    )