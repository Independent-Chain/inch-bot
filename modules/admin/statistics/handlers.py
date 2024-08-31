from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.table import Admin
from modules.admin import AdminModule
from utils import Markdown as md, Translator


@AdminModule.router.callback_query(F.data == "statistics")
async def h_statistics(callback: CallbackQuery, state: FSMContext) -> None:

    strings: dict[str, dict] = {
        "statistics": {
            "ru": (f"{md.bold('Пользователей')}: {Admin.users()}\n"
                   f"{md.bold('Майнеров')}: {Admin.miners()}\n"
                   f"{md.bold('Добыто монет')}: {round(Admin.points(), 3)}\n"
                   f"{md.bold('Доступно промокодов')}: {Admin.codes()}"),
            "en": (f"{md.bold('Users')}: {Admin.users()}\n"
                   f"{md.bold('Miners')}: {Admin.miners()}\n"
                   f"{md.bold('Coins mined')}: {round(Admin.points(), 3)}\n"
                   f"{md.bold('Promo codes available')}: {Admin.codes()}")
        }
    }

    await callback.answer(show_alert=False)

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "statistics"),
        reply_markup=AdminModule.modules["statistics"].keyboard(callback)
    )