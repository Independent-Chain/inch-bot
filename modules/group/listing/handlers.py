from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from modules.group import GroupModule
from utils import Markdown as md, TonSpace, Translator


@GroupModule.router.message(Command("listing"))
async def h_listing(message: Message, state: FSMContext) -> None:

    balance: float = await TonSpace.balance()

    strings: dict[str, dict] = {
        "support": {
            "ru": (f"Согласно {md.url('официальной документации', 'https://docs.google.com/forms/d/e/1FAIpQLSf4g-MB6BBYi8SVcloxAEc4tXQ-4034ngTEGjIsyaqGscjl8w/viewform?pli=1')} "
                   f"децентрализованной биржи DeDust.io для размещения на бирже требуется первоначальный капитал в "
                   f"размере 2000 {md.bold('TON')} или {md.bold('USDT')} в соответствующем эквиваленте.\n"
                   f"\n"
                   f"{md.bold('Собрано')}: {balance} TON\n"
                   f"{md.bold('Осталось собрать')}: {2000 - balance} TON"),
            "en": (f"According to the {md.url('official documentation', 'https://docs.google.com/forms/d/e/1FAIpQLSf4g-MB6BBYi8SVcloxAEc4tXQ-4034ngTEGjIsyaqGscjl8w/viewform?pli=1')} "
                   f"of the decentralized exchange DeDust.io initial capital in the amount of "
                   f"2000 {md.bold('TON')} or {md.bold('USDT')} in the corresponding equivalent is required for listing.\n"
                   f"\n"
                   f"{md.bold('Collected')}: {balance} TON\n"
                   f"{md.bold('It remains to collect')}: {2000 - balance} TON")
        }
    }

    await message.answer(
        text=Translator.text(message, strings, "support"),
        reply_markup=GroupModule.modules["listing"].keyboard(message)
    )
    return None