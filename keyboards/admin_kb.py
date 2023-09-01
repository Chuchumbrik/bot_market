from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

b_add_product = KeyboardButton('Добавить товар')
b_delete_product = KeyboardButton('/Удалить')
b_change_access_level_test = KeyboardButton('Change access')

kb_admin_global = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin_global.row(b_add_product, b_delete_product, b_change_access_level_test)

ib_prev_add_product = InlineKeyboardButton('Назад', callback_data='previous')
ib_cancel_add_product = InlineKeyboardButton('Отмена', callback_data='cancel')
kb_ib_admin_add = InlineKeyboardMarkup()
kb_ib_admin_add.row(ib_prev_add_product, ib_cancel_add_product)

ib_is_hidden_yes_add_product = InlineKeyboardButton('Да', callback_data='is_hidden_yes')
ib_is_hidden_no_add_product = InlineKeyboardButton('Нет', callback_data='is_hidden_no')
kb_ib_ih_admin_add = InlineKeyboardMarkup()
kb_ib_ih_admin_add.row(ib_is_hidden_yes_add_product, ib_is_hidden_no_add_product)
kb_ib_ih_admin_add.row(ib_prev_add_product, ib_cancel_add_product)

kb_admin_add_edit = InlineKeyboardMarkup()
kb_admin_add_edit.add(ib_cancel_add_product)


ib_photo_edit_product = InlineKeyboardButton('Фото', callback_data='edit_photo')
ib_name_edit_product = InlineKeyboardButton('Название', callback_data='edit_name')
ib_description_edit_product = InlineKeyboardButton('Описание', callback_data='edit_description')
ib_price_edit_product = InlineKeyboardButton('Цена', callback_data='edit_price')
ib_count_edit_product = InlineKeyboardButton('Количество', callback_data='edit_count')
ib_is_hidden_edit_product = InlineKeyboardButton('Видимость', callback_data='edit_is_hidden')
ib_cancel_edit_product = InlineKeyboardButton('Сохранить', callback_data='edit_cancel')

kb_admin_edit = InlineKeyboardMarkup()
kb_admin_edit.row(ib_photo_edit_product, ib_name_edit_product)
kb_admin_edit.row(ib_description_edit_product, ib_price_edit_product,)
kb_admin_edit.row(ib_count_edit_product, ib_is_hidden_edit_product)
kb_admin_edit.row(ib_cancel_edit_product)

kb_admin_edit_load = InlineKeyboardMarkup()
kb_admin_edit_load.row(ib_cancel_add_product)
