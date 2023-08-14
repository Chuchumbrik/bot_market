from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/catalog')
b2 = KeyboardButton('/start')

kb_client = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)

kb_client.row(b2, b1)