import asyncio
import logging

from core.config import bot, dispatcher
from modules.main import MainModule

# Comment down string for off logging.
logging.basicConfig(level=logging.INFO)

dispatcher.include_routers(MainModule.router)


async def main() -> None:
    bot_task = asyncio.create_task(bot.delete_webhook(drop_pending_updates=True))
    dispatcher_task = asyncio.create_task(dispatcher.start_polling(bot))

    await bot_task
    await dispatcher_task



if __name__ == "__main__":
    while True:
        asyncio.run(main())