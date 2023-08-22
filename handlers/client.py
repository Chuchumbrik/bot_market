from aiogram import types, Dispatcher
from aiogram.dispatcher import filters
from create_bot import dp, bot
from data_base import sqlite_db, sqlite_db_user
from keyboards import kb_client
from dictionaries.dictionaries_commands import DICTIONARY_CATALOG


async def commands_start(message: types.Message):
    try:
        check_exists_user = await sqlite_db.check_exists_user(message.from_user.username)
        if check_exists_user is not True:
            await sqlite_db.add_user(message.from_user.username)
        await message.reply('Чего надо то?', reply_markup=kb_client)
    except Exception as e:
        await message.reply(f'Общение с ботом через ЛС, напишите ему: \nhttps://t.me/tryYourBot \n{e}')


async def get_catalog_product(message: types.Message):
    check_exists_products = sqlite_db_user.check_exists_product_catalog_user()
    if check_exists_products:
        catalog_products = await sqlite_db_user.get_product_catalog_user()
        for ret in catalog_products:
            await bot.send_photo(message.from_user.id, ret[1], f'{ret[2]}\nОписание: {ret[3]}\nЦена: {ret[4]}\nКоличество: {ret[6]}')
    else:
        await message.answer('В данный момент товаров нет', reply_markup=kb_client.kb_admin_global)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])

    dp.register_message_handler(get_catalog_product, filters.Text(endswith=DICTIONARY_CATALOG, ignore_case=True))
