import asyncio
import logging

from core.config import bot, dispatcher
from modules.main import MainModule
from modules.group import GroupModule
from modules.admin import AdminModule

from utils.storage_checker import StorageChecker

# Comment down string for off logging.
logging.basicConfig(level=logging.INFO)

dispatcher.include_routers(MainModule.router, GroupModule.router, AdminModule.router)


async def main() -> None:
    bot_task = asyncio.create_task(bot.delete_webhook(drop_pending_updates=True))
    dispatcher_task = asyncio.create_task(dispatcher.start_polling(bot))
    check_storage_task = asyncio.create_task(StorageChecker.check_storage())

    await check_storage_task
    await bot_task
    await dispatcher_task



if __name__ == "__main__":
    while True:
        asyncio.run(main())