from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
if os.getenv('TOKEN'):
    bot = Bot(token=os.getenv('TOKEN'))
else:
    bot = Bot(token='6360359150:AAEYsfBtC_mgQqga7qBZY_PUCvxm6Oy8KqI')
dp = Dispatcher(bot, storage=storage)
