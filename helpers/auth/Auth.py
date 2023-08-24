from aiogram.dispatcher import FSMContext
from create_bot import bot
from data_base import sqlite_db
from keyboards import client_kb
from keyboards import admin_kb

class Auth() :
	async def check_access_level(user_name, user_id, state: FSMContext, user_access_level: str):
		check = await Auth.check_access_level_main(user_name,user_id, user_access_level)
		if check is not True and state is not None:
			await state.finish()
		return check

	async def check_access_level_main(user_name, user_id, user_access_level):
		access_level = await sqlite_db.get_access_level(user_name)
		print(f'access_level - {access_level}')
		if access_level == user_access_level:
			return True
		else :
			if access_level == 'admin' :
				await sqlite_db.add_admin(user_name)
				await bot.send_message(user_id, "Вы стали админом", reply_markup = admin_kb.kb_admin_global)
			else :
				await sqlite_db.delete_admin(user_name)
				await bot.send_message(user_id, "Вы стали пользователем", reply_markup = client_kb.kb_client)
			return False


