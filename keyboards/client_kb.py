from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('/catalog')
b2 = KeyboardButton('/start')
button_change_access_level = KeyboardButton('Change access')

kb_client = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)

kb_client.row(b2, b1, button_change_access_level)