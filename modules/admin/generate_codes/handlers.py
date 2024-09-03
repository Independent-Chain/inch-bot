from aiogram import F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database import t_codes
from modules.admin import AdminModule
from states import AdminStates
from utils import Markdown as md, Translator


@AdminModule.router.callback_query(F.data == "generate_codes")
async def h_generate(callback: CallbackQuery, state: FSMContext) -> None:

    strings: dict[str, dict] = {
        "generate": {
            "ru": (f"{md.bold('Шаблон для генерации')}:\n"
                   f"{md.monospaced('активации:сумма')}"),
            "en": (f"{md.bold('Template to generate')}:\n"
                   f"{md.monospaced('activation:amount')}")
        }
    }

    await callback.answer(show_alert=False)
    await state.set_state(AdminStates.generate_codes)
    await state.update_data(anchor=callback.message.message_id)

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "generate"),
        reply_markup=AdminModule.modules["generate_codes"].keyboard(callback, "back")
    )


@AdminModule.router.message(StateFilter(AdminStates.generate_codes))
async def h_generate_template(message: Message, state: FSMContext, bot: Bot) -> None:

    template: list = message.text.split(":")
    activations: int = int(template[0])
    value: float = float(template[1])
    code: str = t_codes.generate(activations, value)

    strings: dict[str, dict] = {
        "code": {
            "ru": (f"{activations} активаций по {value} $tINCH\n"
                   f"{md.monospaced(code)}"),
            "en": (f"{activations} activations with {value} $tINCH\n"
                   f"{md.monospaced(code)}")
        }
    }

    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id
    )

    state_data: dict = await state.get_data()

    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=state_data["anchor"],
        text=Translator.text(message, strings, "code"),
        reply_markup=AdminModule.modules["generate_codes"].keyboard(message, "close")
    )