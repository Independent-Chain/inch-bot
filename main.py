import asyncio
import logging

from config.config import Config, load_config
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from modules.main import MainModule
from modules.group import GroupModule
from modules.admin import AdminModule

from utils.storage_checker import StorageChecker

# Comment down string for off logging.
logging.basicConfig(level=logging.INFO)


async def main() -> None:
    config: Config = load_config()
    API_TOKEN = config.secrets.token

    bot: Bot = Bot(
        token=API_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dispatcher: Dispatcher = Dispatcher()

    bot_task = asyncio.create_task(bot.delete_webhook(drop_pending_updates=True))
    dispatcher_task = asyncio.create_task(dispatcher.start_polling(bot))
    check_storage_task = asyncio.create_task(StorageChecker.check_storage(bot))

    dispatcher.include_routers(MainModule.router, GroupModule.router, AdminModule.router)

    await check_storage_task
    await bot_task
    await dispatcher_task


if __name__ == "__main__":
    while True:
        asyncio.run(main())
