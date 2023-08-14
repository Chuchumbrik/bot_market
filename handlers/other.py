from aiogram import types, Dispatcher  
from create_bot import dp 
from keyboards import admin_kb

async def error_command(message : types.Message) :
	await message.answer(f'Нет такой команды {message.text}', reply_markup = admin_kb.kb_admin_global)
	await message.delete()
	

def register_handlers_other(dp : Dispatcher) :
	dp.register_message_handler(error_command)