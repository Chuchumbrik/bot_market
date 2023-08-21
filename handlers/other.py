from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext  
from create_bot import dp 
from keyboards import admin_kb, client_kb, kb_admin_global, kb_client
from data_base import sqlite_db



async def error_command(message : types.Message) :
	await message.answer(f'Нет такой команды {message.text}', reply_markup = admin_kb.kb_admin_global)
	await message.delete()
	

def register_handlers_other(dp : Dispatcher) :
	dp.register_message_handler(error_command)