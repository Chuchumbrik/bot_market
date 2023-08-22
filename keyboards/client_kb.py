from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_list_product = KeyboardButton('Список товаров')

button_change_access_level_test = KeyboardButton('Change access')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.row(button_list_product, button_change_access_level_test)
