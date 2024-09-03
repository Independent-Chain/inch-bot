import asyncio

from aiogram import F
from aiogram.types import CallbackQuery
from pytonconnect import TonConnect
from pytonconnect.storage import FileStorage
from tonsdk.utils import Address

from config.config import Config, load_config
from database import t_users
from modules.main import MainModule
from utils import Markdown as md, Translator


async def tonspace(connector) -> str:
    wallets: list = connector.get_wallets()
    return await connector.connect(wallets[0])


async def tonkeeper(connector) -> str:
    wallets: list = connector.get_wallets()
    return await connector.connect(wallets[1])


async def mytonwallet(connector) -> str:
    wallets: list = connector.get_wallets()
    return await connector.connect(wallets[2])


async def connect(connector, user_id: int):
    for i in range(300):
        await asyncio.sleep(1)
        if connector.connected:
            if connector.account.address:
                address: str = Address(connector.account.address).to_string(is_user_friendly=True, is_url_safe=True,
                                                                            is_bounceable=False)

                # Check wallet unique.
                result = t_users.select(("wallet", ), "wallet", address)
                if result is None:
                    t_users.assign("wallet", address, "user_id", user_id)
                    return True
                else:
                    return False


@MainModule.router.callback_query(F.data == "wallet")
async def h_wallet(callback: CallbackQuery) -> None:
    address: str = t_users.select(("wallet",), "user_id", callback.from_user.id)

    strings: dict[str, dict] = {
        "linked": {
            "ru": (f"К вашему профилю уже привязан адрес кошелька: {md.monospaced(f'{address}')}\n"
                   f"\n"
                   f"Для привязки нового адреса обратитесь в поддержку."),
            "en": f"Your wallet address is already linked to your profile: {md.monospaced(f'{address}')}\n"
                  f"\n"
                  f"To link a new address, contact support."
        },
        "not linked": {
            "ru": (f"Для привязки кошелька воспользуйтесь соответствующей кнопкой.\n"
                   f"\n"
                   f"Обращаем внимание на то, что бот поддерживает только адреса {md.bold('TON')} кошельков ⚠️"),
            "en": (f"To link wallet use the appropriate button.\n"
                   f"\n"
                   f"Please note that the bot only supports {md.bold('TON')} wallets addresses ⚠️")
        }
    }

    await callback.answer(show_alert=False)

    if address == "NULL":
        await callback.message.edit_text(
            text=Translator.text(callback, strings, "not linked"),
            reply_markup=MainModule.modules["wallet"].keyboard(callback),
        )
    else:
        await callback.message.edit_text(
            text=Translator.text(callback, strings, "linked"),
            reply_markup=MainModule.modules["wallet"].keyboard_linked(callback),
        )


@MainModule.router.callback_query(F.data == "tonspace")
async def h_wallet_tonspace(callback: CallbackQuery) -> None:
    config: Config = load_config()

    strings: dict[str, dict] = {
        "tonspace": {
            "ru": "Для подключения кошелька TonSpace к вашему профилю воспользуйтесь кнопкой ниже.",
            "en": "To connect the TonSpace wallet to your profile, use the button below."
        },
        "success": {
            "ru": f"Адрес кошелька успешно привязан к вашему профилю ✅",
            "en": f"The wallet address has been successfully linked to your profile ✅"
        },
        "fail": {
            "ru": ("Данный адрес кошелька уже зарегистрирован в системе 🚫\n"
                   "\n"
                   "Если вы не осуществляли привязку данного кошелька обратитесь в поддержку."),
            "en": ("This wallet address has already been registered in system 🚫\n"
                   "\n"
                   "If you have not linked this wallet, contact support.")
        }
    }

    await callback.answer(show_alert=False)

    connector = TonConnect(
        manifest_url='https://raw.githubusercontent.com/diominvd/independent_chain_bot/main/modules/main/wallet/manifest.json',
        storage=FileStorage(config.secrets.wallet_storage_path + f"storage/{callback.from_user.id}.json")
    )

    connect_url: str = await tonspace(connector)

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "tonspace"),
        reply_markup=MainModule.modules["wallet"].keyboard_connect_tonspace(callback, connect_url)
    )

    if await connect(connector, callback.from_user.id):
        await callback.message.edit_text(
            text=Translator.text(callback, strings, "success"),
            reply_markup=MainModule.modules["wallet"].keyboard_connected(callback)
        )
    else:
        await callback.message.edit_text(
            text=Translator.text(callback, strings, "fail"),
            reply_markup=MainModule.modules["wallet"].keyboard_connected_error(callback)
        )


@MainModule.router.callback_query(F.data == "tonkeeper")
async def h_wallet_tonkeeper(callback: CallbackQuery) -> None:
    config: Config = load_config()

    strings: dict[str, dict] = {
        "tonspace": {
            "ru": "Для подключения кошелька Tonkeeper к вашему профилю воспользуйтесь кнопкой ниже.",
            "en": "To connect the Tonkeeper wallet to your profile, use the button below."
        },
        "success": {
            "ru": f"Адрес кошелька успешно привязан к вашему профилю ✅",
            "en": f"The wallet address has been successfully linked to your profile ✅"
        },
        "fail": {
            "ru": ("Данный адрес кошелька уже зарегистрирован в системе 🚫\n"
                   "\n"
                   "Если вы не осуществляли привязку данного кошелька обратитесь в поддержку."),
            "en": ("This wallet address has already been registered in system 🚫\n"
                   "\n"
                   "If you have not linked this wallet, contact support.")
        }
    }

    await callback.answer(show_alert=False)

    connector = TonConnect(
        manifest_url='https://raw.githubusercontent.com/diominvd/independent_chain_bot/main/modules/main/wallet/manifest.json',
        storage=FileStorage(config.secrets.wallet_storage_path + f"storage/{callback.from_user.id}.json")
    )

    connect_url: str = await tonkeeper(connector)

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "tonspace"),
        reply_markup=MainModule.modules["wallet"].keyboard_connect_tonkeeper(callback, connect_url)
    )

    if await connect(connector, callback.from_user.id):
        await callback.message.edit_text(
            text=Translator.text(callback, strings, "success"),
            reply_markup=MainModule.modules["wallet"].keyboard_connected(callback)
        )
    else:
        await callback.message.edit_text(
            text=Translator.text(callback, strings, "fail"),
            reply_markup=MainModule.modules["wallet"].keyboard_connected_error(callback)
        )


@MainModule.router.callback_query(F.data == "mytonwallet")
async def h_wallet_mytonwallet(callback: CallbackQuery) -> None:
    config: Config = load_config()

    strings: dict[str, dict] = {
        "mytonwallet": {
            "ru": "Для подключения кошелька MyTonWallet к вашему профилю воспользуйтесь кнопкой ниже.",
            "en": "To connect the MyTonWallet wallet to your profile, use the button below."
        },
        "success": {
            "ru": f"Адрес кошелька успешно привязан к вашему профилю ✅",
            "en": f"The wallet address has been successfully linked to your profile ✅"
        },
        "fail": {
            "ru": ("Данный адрес кошелька уже зарегистрирован в системе 🚫\n"
                   "\n"
                   "Если вы не осуществляли привязку данного кошелька обратитесь в поддержку."),
            "en": ("This wallet address has already been registered in system 🚫\n"
                   "\n"
                   "If you have not linked this wallet, contact support.")
        }
    }

    await callback.answer(show_alert=False)

    connector = TonConnect(
        manifest_url='https://raw.githubusercontent.com/diominvd/independent_chain_bot/main/modules/main/wallet/manifest.json',
        storage=FileStorage(config.secrets.wallet_storage_path + f"storage/{callback.from_user.id}.json")
    )

    connect_url: str = await mytonwallet(connector)

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "mytonwallet"),
        reply_markup=MainModule.modules["wallet"].keyboard_connect_mytonwallet(callback, connect_url)
    )

    if await connect(connector, callback.from_user.id):
        await callback.message.edit_text(
            text=Translator.text(callback, strings, "success"),
            reply_markup=MainModule.modules["wallet"].keyboard_connected(callback)
        )
    else:
        await callback.message.edit_text(
            text=Translator.text(callback, strings, "fail"),
            reply_markup=MainModule.modules["wallet"].keyboard_connected_error(callback)
        )
