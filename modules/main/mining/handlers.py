import datetime

from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database import t_mining, t_users
from modules.main import MainModule
from utils import Markdown as md, Translator
from utils.tonspace import TonSpace


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

    language: str = t_users.select(("language",), "user_id", callback.from_user.id)
    seconds: float = time
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


@MainModule.router.callback_query(F.data == "mining")
async def h_mining(callback: CallbackQuery, state: FSMContext) -> None:

    user_wallet: str = t_users.select(("wallet", ), "user_id", callback.from_user.id)
    if user_wallet == "NULL":
        strings: dict[str, dict] = {
            "alert": {
                "ru": f"Привяжите кошелёк Ton Space для доступа к добыче.",
                "en": f"Link the Ton Space wallet to access the loot."
            }
        }

        await callback.answer(
            text=Translator.text(callback, strings, "alert"),
            show_alert=True
        )
        return None

    m_user = t_mining.user(callback.from_user.id)
    if m_user is None:
        t_mining.insert(
            user_id=callback.from_user.id,
            username=callback.from_user.username,
            last_claim=datetime.datetime.now(),
            reactor=1,
            storage=1,
            bot=0.0,
            booster=1.0
        )

    await callback.answer(show_alert=False)

    user = t_users.user(callback.from_user.id)
    m_user = t_mining.user(callback.from_user.id)

    # Update booster value.
    m_user.booster = TonSpace.booster(callback.from_user.id)

    # Calculate time from last claim (in seconds).
    time_difference: float = (datetime.datetime.now() - m_user.last_claim).total_seconds()

    strings: dict[str, dict] = {
        "mining": {
            "ru": (f"{md.bold('Баланс')}: {user.balance} $tINCH\n"
                   f"{md.bold('Последний сбор')}: {format_time(callback, time_difference)} назад\n"
                   f"{md.bold('Скорость добычи')}: {round(m_user.reactor * 0.001 * 3600 * m_user.booster, 3)} $tINCH в час\n"
                   f"{md.bold('Усилитель добычи')}: x{m_user.booster}\n"
                   f"\n"
                   f"Обращаем внимание ⚠️ Для корректной работы добычи все приобретённые усилители должны "
                   f"храниться на кошельке в сети TON.\n"
                   f"\n"
                   f"Для комфортного использования раздела \"Добыча\" настоятельно рекомендуем ознакомиться "
                   f"с {md.url('данным руководством', 'https://teletype.in/@inch_ton/inch_mining_ru')}."),
            "en": (f"{md.bold('Balance')}: {user.balance} $tINCH\n"
                   f"{md.bold('Last claim')}: {format_time(callback, time_difference)} back\n"
                   f"{md.bold('Mining speed')}: {round(m_user.reactor * 0.001 * 3600 * m_user.booster, 3)} $tINCH в час\n"
                   f"{md.bold('Mining booster')}: x{m_user.booster}\n"
                   f"\n"
                   f"Please note that ⚠️ For the correct operation of mining, all purchased amplifiers must "
                   f"be stored on a wallet on the TON network.\n"
                   f"\n"
                   f"For comfortable use of the \"Mining\" section, we strongly recommend that you read"
                   f"{md.url('this manual', 'https://teletype.in/@inch_ton/inch_mining_en')}."),
        }
    }

    try:
        await callback.message.edit_text(
            text=Translator.text(callback, strings, "mining"),
            reply_markup=MainModule.modules["mining"].keyboard(callback),
            disable_web_page_preview=True
        )
    except TelegramBadRequest:
        pass


@MainModule.router.callback_query(F.data == "claim")
async def h_claim(callback: CallbackQuery, state: FSMContext) -> None:

    user = t_mining.user(callback.from_user.id)

    # Update booster value.
    user.booster = TonSpace.booster(callback.from_user.id)

    time_difference: float = (datetime.datetime.now() - user.last_claim).total_seconds()

    if time_difference < user.storage * 3600 + 7200:

        # Update last claim time.
        t_mining.assign("last_claim", datetime.datetime.now(), "user_id", user.user_id)

        # Calculate reward.
        reward: float = user.reactor * 0.001 * time_difference * user.booster

        # Reward accrual.
        t_users.increase("balance", reward, "user_id", user.user_id)

        strings: dict[str, dict] = {
            "alert": {
                "ru": f"Получено {round(reward, 3)} $tICH",
                "en": f"Received {round(reward, 3)} $tICH"
            }
        }

        await callback.answer(
            text=Translator.text(callback, strings, "alert"),
            show_alert=True
        )
    else:

        # Update last claim time.
        t_mining.assign("last_claim", datetime.datetime.now(), "user_id", user.user_id)

        strings: dict[str, dict] = {
            "alert": {
                "ru": "Ресурсы сгорели. Процесс добычи перезапущен.",
                "en": "The resources are burned out. The mining process has been restarted."
            }
        }

        await callback.answer(
            text=Translator.text(callback, strings, "alert"),
            show_alert=True
        )

    await h_mining(callback, state)