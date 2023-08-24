from aiogram import types, Dispatcher
from data_base import sqlite_db
from keyboards import client_kb, admin_kb


async def change_access_level(message: types.Message):
    access_level = await sqlite_db.get_access_level(message.from_user.username)
    print(f'access_level - {access_level}')
    if access_level == 'admin':
        await sqlite_db.delete_admin(message.from_user.username)
        await message.reply("Вы стали пользователем", reply_markup=client_kb.kb_client)
    else:
        await sqlite_db.add_admin(message.from_user.username)
        await message.reply("Вы стали админом", reply_markup=admin_kb.kb_admin_global)


def register_handlers_test(dp: Dispatcher):
    dp.register_message_handler(change_access_level, lambda x: x.text and x.text.startswith('Change access'))