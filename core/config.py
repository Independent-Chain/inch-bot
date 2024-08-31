from aiogram import Bot, Dispatcher
from core.secrets import API_TOKEN


bot: Bot = Bot(token=API_TOKEN, parse_mode="html")
dispatcher: Dispatcher = Dispatcher()