from aiogram import types, Dispatcher  
from create_bot import dp, bot
from data_base import sqlite_db
from keyboards import kb_client


async def commands_start(message : types.Message) :
	try:
		await bot.send_message(message.from_user.id, 'Приятного аппетита', reply_markup = kb_client)
		await message.delete()
	except Exception as e:
		await message.reply(f'Общение с ботом через ЛС, напишите ему: \nhttps://t.me/tryYourBot \n{e}')

async def get_catalog_product(message : types.Message) :
	catalog_product = await sqlite_db.get_product_catalog()
	for ret in catalog_product :
		await bot.send_photo(message.from_user.id, ret[1], f'{ret[2]}\nОписание: {ret[3]}\nЦена: {ret[4]}')

def register_handlers_client(dp : Dispatcher) :
	dp.register_message_handler(commands_start, commands = ['start', 'help'])
	dp.register_message_handler(get_catalog_product, commands = ['catalog', 'Каталог'])