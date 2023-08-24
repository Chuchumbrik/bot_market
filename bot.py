from aiogram.utils import executor
from create_bot import dp
from data_base import sqlite_start
from handlers import client, admin_all, other, helper_test
from handlers.admin import add_product


async def on_startup(_):
    print('Bot is online')
    sqlite_start.sql_start()

helper_test.register_handlers_test(dp)
client.register_handlers_client(dp)
admin_all.register_handlers_admin(dp)
add_product.register_handlers_admin_add(dp)
other.register_handlers_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
