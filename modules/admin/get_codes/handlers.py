from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database import t_codes
from modules.admin import AdminModule
from utils import Markdown as md


@AdminModule.router.callback_query(F.data == "get_codes")
async def h_get(callback: CallbackQuery, state: FSMContext) -> None:

    await callback.answer(show_alert=False)

    codes: list = t_codes.get()

    text: str = f""
    for code in codes:
        text += f"{md.monospaced(str(code[0]))} - {code[1]} - {code[2]}\n"

    await callback.message.edit_text(
        text=text,
        reply_markup=AdminModule.modules["get_codes"].keyboard(callback)
    )