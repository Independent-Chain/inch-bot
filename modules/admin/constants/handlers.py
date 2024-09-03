from aiogram import F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database import t_users, t_mining
from modules.admin import AdminModule
from states import AdminStates
from utils import Markdown as md, Translator


@AdminModule.router.callback_query(F.data == "constants")
async def h_constants(callback: CallbackQuery, state: FSMContext) -> None:

    strings: dict[str, dict] = {
        "constants": {
            "ru": (f"{md.bold('Текущие константы')}:\n"
                   f"{md.bold('Начальный баланс')} (start): {t_users.start}\n"
                   f"{md.bold('Награда за друга')} (referal): {t_users.referal}\n"
                   f"{md.bold('Глобальный множитель')} (booster): {t_mining.booster}\n"
                   f"{md.bold('Скидка на улучшения')} (discount): {t_mining.discount}\n"
                   f"\n"
                   f"{md.monospaced('имя константы = значение')}"),
            "en": (f"{md.bold('Current constants')}:\n"
                   f"{md.bold('Start balance')} (start): {t_users.start}\n"
                   f"{md.bold('Referal reward')} (referal): {t_users.referal}\n"
                   f"{md.bold('Global booster')} (booster): {t_mining.booster}\n"
                   f"{md.bold('Upgrades discount')} (discount): {t_mining.discount}\n"
                   f"\n"
                   f"{md.monospaced('constant name = value')}")
        }
    }

    await callback.answer(show_alert=False)
    await state.set_state(AdminStates.constants)
    await state.update_data(anchor=callback.message.message_id)

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "constants"),
        reply_markup=AdminModule.modules["constants"].keyboard(callback, "back")
    )


@AdminModule.router.message(StateFilter(AdminStates.constants))
async def h_constants_template(message: Message, state: FSMContext, bot: Bot) -> None:

    template: list = message.text.split("=")
    name: str = template[0]
    value: float = template[1]

    match name:
        case "start":
            t_users.start = value
        case "referal":
            t_users.referal = value
        case "booster":
            t_mining.booster = value
        case "discount":
            t_mining.discount = value

    strings: dict[str, dict] = {
        "notify": {
            "ru": f"Значение {value} установлено для константы {name}.",
            "en": f"The value {value} is set for the constant {name}."
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
        text=Translator.text(message, strings, "notify"),
        reply_markup=AdminModule.modules["constants"].keyboard(message, "close")
    )
