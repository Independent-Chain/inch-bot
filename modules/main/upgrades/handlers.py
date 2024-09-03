from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database import t_mining, t_users
from modules.main import MainModule
from utils import Markdown as md, Translator


def format_time_ru(hours: int) -> str:
    if hours == 1:
        return f"{hours} час"
    elif 2 <= hours <= 4:
        return f"{hours} часа"
    elif 5 <= hours:
        return f"{hours} часов"


def format_time_en(hours: int) -> str:
    if hours == 1:
        return f"{hours} hour"
    elif 2 <= hours:
        return f"{hours} hours"


@MainModule.router.callback_query(F.data == "upgrades")
async def h_upgrades(callback: CallbackQuery) -> None:

    user = t_users.user(callback.from_user.id)
    m_user = t_mining.user(callback.from_user.id)

    strings: dict[str, dict] = {
        "upgrades": {
            "ru": (f"Улучшения позволяют увеличить количество добываемых $tINCH.\n"
                   f"\n"
                   f"⚙️ {md.bold('Реактор')}: {m_user.reactor} уровень ({m_user.reactor * 0.001}/сек)\n"
                   f"🕑 {md.bold('Хранилище')}: {m_user.storage} уровень ({format_time_ru(m_user.storage)})\n"
                   f"🤖 {md.bold('Автосбор')}: Выключен\n"
                   f"\n"
                   f"{md.bold('Баланс')}: {user.balance} $tINCH\n"
                   f"\n"
                   f"{md.bold('Стоимость улучшений')}:\n"
                   f"{md.bold('Реактор')} ({(m_user.reactor + 1) * 0.001}/сек): {t_mining.upgrade_price('reactor', m_user.reactor)} $tINCH\n"
                   f"{md.bold('Хранилище')} ({format_time_ru(m_user.storage + 1)}): {t_mining.upgrade_price('storage', m_user.storage)} $tINCH"),
            "en": (f"Improvements allow you to increase the amount of $tINCH mined.\n"
                   f"\n"
                   f"⚙️ {md.bold('Reactor')}: {m_user.reactor} level ({m_user.reactor * 0.001}/сек)\n"
                   f"🕑 {md.bold('Storage')}: {m_user.storage} level ({format_time_en(m_user.storage)})\n"
                   f"🤖 {md.bold('Autoclaim')}: Off\n"
                   f"\n"
                   f"{md.bold('Balance')}: {user.balance} $tINCH\n"
                   f"\n"
                   f"{md.bold('Cost of improvements')}:\n"
                   f"{md.bold('Reactor')} ({(m_user.reactor + 1) * 0.001}/sec): {t_mining.upgrade_price('reactor', m_user.reactor)} $tINCH\n"
                   f"{md.bold('Storage')} ({format_time_en(m_user.storage + 1)}): {t_mining.upgrade_price('storage', m_user.storage)} $tINCH"),
        }
    }

    await callback.answer(show_alert=False)

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "upgrades"),
        reply_markup=MainModule.modules["upgrades"].keyboard(callback)
    )


@MainModule.router.callback_query(F.data == "upgrade_reactor")
async def h_upgrade_reactor(callback: CallbackQuery, state: FSMContext) -> None:

    user = t_users.user(callback.from_user.id)
    m_user = t_mining.user(callback.from_user.id)

    reactor_price: float = t_mining.upgrade_price("reactor", m_user.reactor)

    if user.balance < reactor_price:

        strings: dict[str, dict] = {
            "failed": {
                "ru": "Недостаточно $tINCH для улучшения реактора",
                "en": "Not enough $tINCH to improve the reactor"
            }
        }

        await callback.answer(
            text=Translator.text(callback, strings, "failed"),
            show_alert=True
        )

    else:

        t_users.decrease("balance", reactor_price, "user_id", user.user_id)
        t_mining.increase("reactor", 1, "user_id", m_user.user_id)

        strings: dict[str, dict] = {
            "success": {
                "ru": f"Уровень реактора повышен до {m_user.reactor + 1}",
                "en": f"Reactor level increased to {m_user.reactor + 1}"
            }
        }

        await callback.answer(
            text=Translator.text(callback, strings, "success"),
            show_alert=True
        )

        await h_upgrades(callback, state)


@MainModule.router.callback_query(F.data == "upgrade_storage")
async def h_upgrade_storage(callback: CallbackQuery, state: FSMContext) -> None:

    user = t_users.user(callback.from_user.id)
    m_user = t_mining.user(callback.from_user.id)

    storage_price: float = t_mining.upgrade_price("storage", m_user.storage)

    if user.balance < storage_price:

        strings: dict[str, dict] = {
            "failed": {
                "ru": "Недостаточно $tINCH для улучшения хранилища",
                "en": "Not enough $tINCH to improve the storage"
            }
        }

        await callback.answer(
            text=Translator.text(callback, strings, "failed"),
            show_alert=True
        )

    else:

        t_users.decrease("balance", storage_price, "user_id", user.user_id)
        t_mining.increase("storage", 1, "user_id", m_user.user_id)

        strings: dict[str, dict] = {
            "success": {
                "ru": f"Уровень хранилища повышен до {m_user.storage + 1}",
                "en": f"Storage level increased to {m_user.storage + 1}"
            }
        }

        await callback.answer(
            text=Translator.text(callback, strings, "success"),
            show_alert=True
        )

        await h_upgrades(callback, state)
