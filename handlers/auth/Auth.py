from aiogram.dispatcher import FSMContext 
from multipledispatch import dispatch
from aiogram import types

class Auth() :
	@dispatch(types.Message, FSMContext, str)
	def check_access_level(message, state, user_access_level) :
		check = check_access_level_main(message, user_access_level)
		if check is not True:
			state.finish()
		return check

	@dispatch(types.Message, str)
	def check_access_level(message, user_access_level) :
		return check_access_level_main(message, user_access_level)

	def check_access_level_main(message : types.Message, user_access_level) :
		access_level = sqlite_db.get_access_level(message.from_user.username)
		print(f'access_level - {access_level}')
		if access_level == user_access_level :
			return True
		else :
			if access_level == 'admin' :
				sqlite_db.add_admin(message.from_user.username)
				message.reply("Вы стали админом", reply_markup = admin_kb.kb_admin_global)
			else :
				sqlite_db.delete_admin(message.from_user.username)
				message.reply("Вы стали пользователем", reply_markup = client_kb.kb_client)
			return False