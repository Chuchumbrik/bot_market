from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher  
from create_bot import dp, bot
from data_base import sqlite_db
from keyboards import admin_kb, kb_admin_edit, kb_admin_edit_load
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from multipledispatch import dispatch

ID = None

class FSMAddProducts(StatesGroup) :
    photo = State()
    name = State()
    description = State()
    price = State()

async def make_changes_command(message : types.Message) :
	global ID 
	ID = message.from_user.id
	await bot.send_message(message.from_user.id, "Что делаем сегодня?", reply_markup = admin_kb.kb_admin_global)
	await message.delete()

async def start_load_product(message : types.Message, state : FSMContext) :
	if message.from_user.id == ID :
		print("None")
		await FSMAddProducts.photo.set()
		await delete_inline_button_message(message, state)
		msg = await send_text_state(message, state)
		async with state.proxy() as data:
			data['message_id'] = msg.message_id
			data['state'] = 'FSMAddProducts'

async def cancel_callback_load_product(callback_query : types.CallbackQuery, state : FSMContext) :
	if callback_query.from_user.id :
		print("Отмена")
		current_state = await state.get_state()
		await delete_inline_button_callback(callback_query)
		if current_state is None :
			return 
		async with state.proxy() as data:
			this_state_group = data['state']
		if this_state_group == 'FSMAddProducts' :
			await state.finish()
			await bot.send_message(callback_query.from_user.id, 'Операция отменена', reply_markup = admin_kb.kb_admin_global)
		else : 
			await edit_product_main(state)
		await callback_query.answer()

async def prev_callback_load_product(callback_query : types.CallbackQuery, state : FSMContext) :
	if callback_query.from_user.id :
		print("Назад")
		current_state = await state.get_state()
		if current_state is None :
			return
		if current_state == "FSMAddProducts:photo":
			await cancel_callback_load_product(callback_query, state)
			await callback_query.answer()
			return
		await FSMAddProducts.previous()
		await bot.send_message(callback_query.from_user.id, 'Вернулись на шаг назад')
		msg = await send_text_state(callback_query, state)
		async with state.proxy() as data:
			data['message_id'] = msg.message_id
		await callback_query.answer()


async def load_product_photo(message : types.Message, state : FSMContext) :
	if message.from_user.id == ID :
		print("photo")
		try :
			if message.content_type != 'photo':
				raise Exception('И вот как я должен это записать как картинку?')

			async with state.proxy() as data :
				data['photo'] = message.photo[0].file_id
			await delete_inline_button_message(message, state)

			await FSMAddProducts.next()
			msg = await send_text_state(message, state)
			async with state.proxy() as data:
					data['message_id'] = msg.message_id
		except Exception as err :
			await message.reply(err)
			print(err)


async def load_product_name(message : types.Message, state : FSMContext) :
	if message.from_user.id == ID :
		print("name")
		try :
			await check_valid_text(message.text)

			async with state.proxy() as data : 
				data['name'] = message.text
			await delete_inline_button_message(message, state)

			await FSMAddProducts.next()
			msg = await send_text_state(message, state)
			async with state.proxy() as data:
					data['message_id'] = msg.message_id
		except Exception as err :
			await message.reply(err)
			print(err)


async def load_product_description(message : types.Message, state : FSMContext) :
	if message.from_user.id == ID :
		print("description")
		try :
			await check_valid_text(message.text)

			async with state.proxy() as data : 
				data['description'] = message.text
			await delete_inline_button_message(message, state)
			await FSMAddProducts.next()
			msg = await send_text_state(message, state)
			async with state.proxy() as data:
					data['message_id'] = msg.message_id
		except Exception as err :
			await message.reply(err)
			print(err)


async def load_product_price(message : types.Message, state : FSMContext) :
	if message.from_user.id == ID :
		print("price")
		try :
			try:
			    float(message.text)
			except ValueError:
			    raise Exception('Мне кажется или в цену затисались буквы?')

			price = round(float(message.text), 2)
			if len(str(price)) > 10 :
				raise Exception('Не думаешь, что это слишком дорого?')


			async with state.proxy() as data : 
				data['price'] = price
				name = data['name']
				
			await delete_inline_button_message(message, state)
			await sqlite_db.add_product_in_catalog(state)
			await message.reply("Продукт успешно добавлен", reply_markup = admin_kb.kb_admin_global)
			new_product = await sqlite_db.get_product_by_name(name)
			await send_product(message.from_user.id, new_product[1], new_product[2], new_product[3], new_product[4])
			await state.finish()
		except Exception as err :
			await message.reply(err)
			print(err)

async def del_call_back_run(callback_query : types.CallbackQuery) :
	id_product = callback_query.data.replace('del ', '')
	check_exists_product = await sqlite_db.check_exists_product_by_id(id_product)
	if check_exists_product :
		name_product = await sqlite_db.get_product_name_by_id(id_product)
		await sqlite_db.delete_product_by_id(id_product)
		await delete_inline_button_callback(callback_query)
		await bot.send_message(callback_query.from_user.id, f'{name_product} удалена.', reply_markup = admin_kb.kb_admin_global)
		await callback_query.answer()
	else :
		await bot.send_message(callback_query.from_user.id, "Продукт уже ранее удален", reply_markup = admin_kb.kb_admin_global)
		await callback_query.answer()

async def delete_item(message : types.Message) :
	if message.from_user.id == ID :
		check_exists_products = await sqlite_db.check_exists_product_catalog()
		if check_exists_products :
			catalog_product = await sqlite_db.get_product_catalog()
			for item in catalog_product :
				msg = await send_product(message.from_user.id, item[1], item[2], item[3], item[4])
				await msg.edit_reply_markup(InlineKeyboardMarkup().row(InlineKeyboardButton('Изменить', callback_data = f'edit {item[0]}'),\
					InlineKeyboardButton('Удалить', callback_data = f'del {item[0]}')))
			await bot.send_message(message.from_user.id, "Нажмите на кнопку 'Удалить' под продуктом, который хотите удалить",\
																							reply_markup = admin_kb.kb_admin_global)
		else :
			await message.answer('В данный момент продуктов нет', reply_markup = admin_kb.kb_admin_global)

@dispatch(types.CallbackQuery, FSMContext)
async def send_text_state(callback_query, state) :
	text_state = await text_by_state(state)
	await delete_inline_button_callback(callback_query, state)
	if text_state != '' :
		async with state.proxy() as data:
			this_state_group = data['state']
		if this_state_group == 'FSMAddProducts' :
			msg = await bot.send_message(callback_query.from_user.id, text_state, reply_markup = admin_kb.kb_admin_load)
		else :
			msg = await bot.send_message(callback_query.from_user.id, text_state, reply_markup = admin_kb.kb_admin_edit_load)
		async with state.proxy() as data:
			data['message_id'] = msg.message_id
			print(data['message_id'])
		return msg

@dispatch(types.Message, FSMContext)
async def send_text_state(message, state) :
	text_state = await text_by_state(state)
	await delete_inline_button_message(message, state)

	if text_state != '' :
		msg = await bot.send_message(message.from_user.id, text_state, reply_markup = admin_kb.kb_admin_load)
		async with state.proxy() as data:
			data['message_id'] = msg.message_id
			print(data['message_id'])
		return msg

async def text_by_state(state : FSMContext) :
	current_state = await state.get_state()
	text_state = 'Нет текста!'
	print(current_state)
	if current_state is None:
		text_state = ''
	if current_state == "FSMAddProducts:photo" or current_state == "FSMEditProducts:photo":
		text_state = 'Загрузи фото'
	if current_state == "FSMAddProducts:name" or current_state == "FSMEditProducts:name":
		text_state = 'Теперь название продукта'
	if current_state == "FSMAddProducts:description" or current_state == "FSMEditProducts:description":
		text_state = 'Теперь описание продукта'
	if current_state == "FSMAddProducts:price" or current_state == "FSMEditProducts:price":
		text_state = 'Теперь цену продукта'

	return text_state

#Удаление inline кнопок у сообщений для типа callback_query
@dispatch(types.CallbackQuery, FSMContext)
async def delete_inline_button_callback(callback_query, state) :
	async with state.proxy() as data:
		try :
			await bot.edit_message_reply_markup(chat_id = callback_query.message.chat.id,\
											message_id = data['message_id'],\
											reply_markup = InlineKeyboardMarkup())
		except Exception as err :
			print('message_id - не существует')

@dispatch(types.CallbackQuery)
async def delete_inline_button_callback(callback_query) :
	try :
		await bot.edit_message_reply_markup(chat_id = callback_query.message.chat.id,\
										message_id = callback_query.message.message_id,\
										reply_markup = InlineKeyboardMarkup())
	except Exception as err :
		print(f'message_id - не существует - {callback_query.message.message_id}')

#Удаление inline кнопок у сообщений для типа message
@dispatch(types.Message, FSMContext)
async def delete_inline_button_message(message, state) :
	async with state.proxy() as data:
		try :
			await bot.edit_message_reply_markup(chat_id = message.chat.id,\
										message_id = data['message_id'],\
										reply_markup = InlineKeyboardMarkup())
		except Exception as err :
			print('message_id - не существует')


#Проверка валидности введенного текста
async def check_valid_text(text) :
	error = ''
	if len(text) > 100 :
		error = 'Капец, оно длинное. Такое даже я читать не стану, а я бот'
	if len(text) < 3 :
		error = 'И вот ты правда думаешь, что так можно это описать?'
	if error != '' :
		raise Exception(f'{error}\nПопробуй ввести заново')

# Отправка продукта в сообщении
async def send_product(message_id, p_photo, p_name, p_description, p_price) :
	message = await bot.send_photo(message_id, p_photo,\
					f'Название: {p_name}\nОписание: {p_description}\nЦена: {p_price} рупи')
	return message



class FSMEditProducts(StatesGroup) :
    start = State()
    photo = State()
    name = State()
    description = State()
    price = State()

async def edit_product(callback_query : types.CallbackQuery, state : FSMContext) :
	if callback_query.from_user.id == ID :
		print("None_edit")
		await bot.send_message(callback_query.from_user.id, "Вы выбрали этот продукт для редактирования :",\
											reply_markup = ReplyKeyboardRemove())
		id_product = callback_query.data.replace('edit ', '')
		async with state.proxy() as data:
			data['edit_product_id'] = id_product
			data['edit_user_id'] = callback_query.from_user.id
			data['state'] = 'FSMEditProducts'
		await edit_product_main(state)
		await callback_query.answer()

async def edit_product_main(state : FSMContext) :
	await FSMEditProducts.start.set()
	print("start_edit")
	async with state.proxy() as data:
		id_product = data['edit_product_id'] 
		id_user = data['edit_user_id']
	check_exists_product = await sqlite_db.check_exists_product_by_id(id_product)
	if check_exists_product :
		edit_product = await sqlite_db.get_product_by_id(id_product)
		msg = await send_product(id_user, edit_product[1], edit_product[2], edit_product[3], edit_product[4])
		await msg.edit_reply_markup(admin_kb.kb_admin_edit)
		async with state.proxy() as data:
			data['message_id'] = msg.message_id
	else : 
		await bot.send_message(id_user, 'Вы кто такие, я вас не знаю, идите нахуй!', reply_markup = admin_kb.kb_admin_global)

async def edit_product_photo(callback_query : types.CallbackQuery, state : FSMContext) :
	if callback_query.from_user.id == ID :
		await FSMEditProducts.photo.set()
		await delete_inline_button_callback(callback_query, state)
		print("photo_edit")
		msg = await send_text_state(callback_query, state)
		async with state.proxy() as data:
				data['message_id'] = msg.message_id

async def edit_product_photo_state(message : types.Message, state : FSMContext) :
	if message.from_user.id == ID :
		print("photo_edit")
		try :
			if message.content_type != 'photo':
				raise Exception('И вот как я должен это записать как картинку?')

			async with state.proxy() as data :
				await sqlite_db.edit_product_photo(data['edit_product_id'], message.photo[0].file_id)
			await delete_inline_button_message(message, state)
			await message.delete()
			await edit_product_main(state)
		except Exception as err :
			await message.reply(err)
			print(err)

async def edit_product_name(callback_query : types.CallbackQuery, state : FSMContext) :
	if callback_query.from_user.id == ID :
		await FSMEditProducts.name.set()
		await delete_inline_button_callback(callback_query, state)
		print("name_edit")
		msg = await send_text_state(callback_query, state)
		async with state.proxy() as data:
				data['message_id'] = msg.message_id

async def edit_product_name_state(message : types.Message, state : FSMContext) :
	if message.from_user.id == ID :
		try :
			await check_valid_text(message.text)
			print("name_edit")
			async with state.proxy() as data :
				await sqlite_db.edit_product_name(data['edit_product_id'], message.text)

			await delete_inline_button_message(message, state)
			#await message.delete()
			await edit_product_main(state)
		except Exception as err :
			await message.reply(err)
			print(err)

async def edit_product_description(callback_query : types.CallbackQuery, state : FSMContext) :
	if callback_query.from_user.id == ID :
		await FSMEditProducts.description.set()
		await delete_inline_button_callback(callback_query, state)
		print("description_edit")
		msg = await send_text_state(callback_query, state)
		async with state.proxy() as data:
				data['message_id'] = msg.message_id

async def edit_product_description_state(message : types.Message, state : FSMContext) :
	if message.from_user.id == ID :
		try :
			await check_valid_text(message.text)
			print("description_edit")
			async with state.proxy() as data :
				await sqlite_db.edit_product_description(data['edit_product_id'], message.text)
			await delete_inline_button_message(message, state)
			#await message.delete()
			await edit_product_main(state)
		except Exception as err :
			await message.reply(err)
			print(err)

async def edit_product_price(callback_query : types.CallbackQuery, state : FSMContext) :
	if callback_query.from_user.id == ID :
		await FSMEditProducts.price.set()
		await delete_inline_button_callback(callback_query, state)
		print("price_edit")
		msg = await send_text_state(callback_query, state)
		async with state.proxy() as data:
				data['message_id'] = msg.message_id


async def edit_product_price_state(message : types.Message, state : FSMContext) :
	if message.from_user.id == ID :
		print("price_edit")
		try :
			price = round(float(message.text), 2)
			if len(str(price)) > 10 :
				raise Exception('Не думаешь, что это слишком дорого?')

			async with state.proxy() as data :
				await sqlite_db.edit_product_price(data['edit_product_id'], message.text)
				
			await delete_inline_button_message(message, state)
			await edit_product_main(state)
		except Exception as err :
			await message.reply(err)
			print(err)

async def cancel_callback_edit_product(callback_query : types.CallbackQuery, state : FSMContext) :
	if callback_query.from_user.id :
		print("cancel_edit")
		current_state = await state.get_state()
		await delete_inline_button_callback(callback_query)
		if current_state is None :
			return
		await state.finish()
		await bot.send_message(callback_query.from_user.id, 'Редактирование завершено', reply_markup = admin_kb.kb_admin_global)
		await callback_query.answer()

async def error_command_state(message : types.Message, state : FSMContext) :
	await message.answer(f'Нет такой команды {message.text}\n')
	await message.delete()
	

def register_handlers_admin(dp : Dispatcher) :
	dp.register_message_handler(start_load_product, commands = ['Загрузить'], state = None)
	dp.register_callback_query_handler(edit_product, lambda x : x.data and x.data.startswith('edit '), state = None)
	dp.register_callback_query_handler(cancel_callback_load_product, lambda x : x.data and x.data.startswith('cancel'), state = "*")
	dp.register_callback_query_handler(prev_callback_load_product, lambda x : x.data and x.data.startswith('previous'), state = "*")
	dp.register_callback_query_handler(cancel_callback_edit_product, lambda x : x.data and x.data.startswith('edit_cancel'), state = "*")

	dp.register_callback_query_handler(edit_product_photo, lambda x : x.data and x.data.startswith('edit_photo'), state = FSMEditProducts.start)
	dp.register_message_handler(edit_product_photo_state, content_types = ['text', 'photo'], state = FSMEditProducts.photo)

	dp.register_callback_query_handler(edit_product_name, lambda x : x.data and x.data.startswith('edit_name'), state = FSMEditProducts.start)
	dp.register_message_handler(edit_product_name_state, state = FSMEditProducts.name)

	dp.register_callback_query_handler(edit_product_description, lambda x : x.data and x.data.startswith('edit_description'), state = FSMEditProducts.start)
	dp.register_message_handler(edit_product_description_state, state = FSMEditProducts.description)

	dp.register_callback_query_handler(edit_product_price, lambda x : x.data and x.data.startswith('edit_price'), state = FSMEditProducts.start)
	dp.register_message_handler(edit_product_price_state, state = FSMEditProducts.price)

	dp.register_message_handler(load_product_photo, content_types = ['text', 'photo'], state = FSMAddProducts.photo)
	dp.register_message_handler(load_product_name, state = FSMAddProducts.name)
	dp.register_message_handler(load_product_description, state = FSMAddProducts.description)
	dp.register_message_handler(load_product_price, state = FSMAddProducts.price)
	dp.register_message_handler(make_changes_command, is_chat_admin = True)
	dp.register_callback_query_handler(del_call_back_run, lambda x : x.data and x.data.startswith('del '))
	dp.register_message_handler(delete_item, commands = ['Удалить'])

	dp.register_message_handler(error_command_state, state = "*")

	