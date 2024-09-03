import datetime

from aiogram import F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database import t_users, t_codes
from modules.main import MainModule
from states import CodesStates
from utils import Translator


def format_time(callback: CallbackQuery, time: float) -> str:
    strings: dict[str, dict] = {
        "hour": {
            "ru": ["час", "часа", "часов"],
            "en": ["hour", "hours", "hours"]
        },
        "minute": {
            "ru": ["минуту", "минуты", "минут"],
            "en": ["minute", "minutes", "minutes"]
        },
        "back": {
            "ru": "назад",
            "en": "back"
        }
    }

    language: str = t_users.select(("language", ), "user_id", callback.from_user.id)
    seconds: float = 86400 - time
    hours = int(seconds // 3600)
    minutes = (seconds % 3600) // 60

    if hours == 1:
        hours_str = f"1 {strings['hour'][language][0]}"
    elif 2 <= hours <= 4:
        hours_str = f"{hours} {strings['hour'][language][1]}"
    elif 21 <= hours <= 24:
        hours_str = f"{hours} {strings['hour'][language][1]}"
    else:
        hours_str = f"{hours} {strings['hour'][language][2]}"

    if minutes == 1:
        minutes_str = f"1 {strings['minute'][language][0]}"
    elif 2 <= minutes <= 4:
        minutes_str = f"{int(minutes)} {strings['minute'][language][1]}"
    else:
        minutes_str = f"{int(minutes)} {strings['minute'][language][2]}"

    if hours == 0:
        return f"{minutes_str}"
    else:
        return f"{hours_str} {minutes_str}"


@MainModule.router.callback_query(F.data == "codes")
async def h_codes(callback: CallbackQuery, state: FSMContext):

    user = t_users.user(callback.from_user.id)
    time_difference: float = (datetime.datetime.now() - user.last_code).total_seconds()

    if time_difference < 86400:
        strings: dict[str, dict] = {
            "limit": {
                "ru": f"Следующая активация будет доступна через\n{format_time(callback, time_difference)}",
                "en": f"Next activation will be available via\n{format_time(callback, time_difference)}"
            }
        }

        await callback.answer(
            text=Translator.text(callback, strings, "limit"),
            show_alert=True
        )

        return None
    else:
        strings: dict[str, dict] = {
            "codes": {
                "ru": f"Отправьте 16-ти значный код для его активации 🔠",
                "en": f"Send a 16-digit code to activate it 🔠"
            }
        }

        await callback.answer(show_alert=False)
        await state.set_state(CodesStates.code)
        await state.update_data(anchor=callback.message.message_id)

        last_code_time: tuple = t_users.select(("user_id",), "user_id", callback.from_user.id)
        if last_code_time is None:
            t_users.assign("last_code", datetime.datetime.now() - datetime.timedelta(days=1), "user_id", callback.from_user.id)

        await callback.message.edit_text(
            text=Translator.text(callback, strings, "codes"),
            reply_markup=MainModule.modules["codes"].keyboard(callback, "back")
        )


@MainModule.router.message(StateFilter(CodesStates.code))
async def h_code(message: Message, state: FSMContext, bot: Bot) -> None:

    signature: str = message.text
    code = t_codes.check(signature)

    state_data: dict = await state.get_data()

    if code is not None:
        strings: dict[str, dict] = {
            "success": {
                "ru": (f"Промокод успешно активирован ✅\n"
                       f"Начислено {code.value} $tINCH"),
                "en": (f"The promo code has been successfully activated ✅\n"
                       f"Accrued {code.value} $tINCH")
            }
        }

        await state.clear()

        t_users.increase("balance", code.value, "user_id", message.from_user.id)
        t_users.assign("last_code", datetime.datetime.now(), "user_id", message.from_user.id)
        t_codes.activate(code)

        await bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=state_data["anchor"],
            text=Translator.text(message, strings, "success"),
            reply_markup=MainModule.modules["codes"].keyboard(message, "back")
        )
    else:
        strings: dict[str, dict] = {
            "invalid": {
                "ru": f"Недействительный промокод 🚫",
                "en": f"Invalid promo code 🚫"
            }
        }
        try:
            await bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=state_data["anchor"],
                text=Translator.text(message, strings, "invalid"),
                reply_markup=MainModule.modules["codes"].keyboard(message, "back")
            )
        except:
            pass

    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id
    )