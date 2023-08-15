from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button_load_product = KeyboardButton('/Загрузить')
button_delete_product = KeyboardButton('/Удалить')

kb_admin_global = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)

kb_admin_global.row(button_load_product, button_delete_product)


i_button_cancel_load_product = InlineKeyboardButton('Отмена', callback_data = 'cancel')
i_button_prev_load_product = InlineKeyboardButton('Назад', callback_data = 'previous')
kb_admin_load = InlineKeyboardMarkup()
kb_admin_load.row(i_button_prev_load_product, i_button_cancel_load_product)


 

#i_button_cancel_delete_product = InlineKeyboardButton(f'Удалить %(name)s', callback_data = f'del ')
#kb_admin_delete = InlineKeyboardMarkup()
#kb_admin_delete.add(i_button_cancel_delete_product)

i_button_photo_edit_product = InlineKeyboardButton('Фото', callback_data = 'edit_photo')
i_button_name_edit_product = InlineKeyboardButton('Название', callback_data = 'edit_name')
i_button_description_edit_product = InlineKeyboardButton('Описание', callback_data = 'edit_description')
i_button_price_edit_product = InlineKeyboardButton('Цена', callback_data = 'edit_price')
i_button_cancel_edit_product = InlineKeyboardButton('Закончить редактирование', callback_data = 'edit_cancel')

kb_admin_edit = InlineKeyboardMarkup()
kb_admin_edit.row(i_button_photo_edit_product, i_button_name_edit_product,\
				 i_button_description_edit_product, i_button_price_edit_product)
kb_admin_edit.row(i_button_cancel_edit_product)

kb_admin_edit_load = InlineKeyboardMarkup()
kb_admin_edit_load.row(i_button_cancel_load_product)