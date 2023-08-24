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


i_button_photo_edit_product = InlineKeyboardButton('Фото', callback_data='edit_photo')
i_button_name_edit_product = InlineKeyboardButton('Название', callback_data='edit_name')
i_button_description_edit_product = InlineKeyboardButton('Описание', callback_data='edit_description')
i_button_price_edit_product = InlineKeyboardButton('Цена', callback_data='edit_price')
i_button_cancel_edit_product = InlineKeyboardButton('Закончить редактирование', callback_data='edit_cancel')

kb_admin_edit = InlineKeyboardMarkup()
kb_admin_edit.row(i_button_photo_edit_product, i_button_name_edit_product, \
                  i_button_description_edit_product, i_button_price_edit_product)
kb_admin_edit.row(i_button_cancel_edit_product)

kb_admin_edit_load = InlineKeyboardMarkup()
kb_admin_edit_load.row(ib_cancel_add_product)
