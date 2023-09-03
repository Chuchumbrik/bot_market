from aiogram import types

from dictionaries.dictionaries_commands import DICTIONARY_ADD_PRODUCT_IS_HIDDEN_YES, DICTIONARY_ADD_PRODUCT_IS_HIDDEN_NO


# Проверка валидности типа фотографии
async def validate_photo(message: types.Message):
    if message.content_type != 'photo':
        raise Exception('И вот как я должен это записать как картинку?')


# Проверка валидности введенного текста
async def validate_text(text):
    error = ''
    if len(text) > 100:
        error = 'Капец, оно длинное. Такое даже я читать не стану, а я бот'
    if len(text) < 3:
        error = 'И вот ты правда думаешь, что так можно это описать?'
    if error != '':
        raise Exception(f'{error}\nПопробуй ввести заново')


# Проверка валидности введенной цены
async def validate_price(text):
    try:
        price = round(float(text), 2)
    except ValueError:
        raise Exception('Мне кажется или в цену затисались буквы / символы?')

    if len(str(price)) > 10:
        raise Exception('Не думаешь, что это слишком дорого?')


# Проверка валидности введенного количества
async def validate_count(text):
    try:
        count = int(text)
    except ValueError:
        raise Exception('Мне кажется или в количество затисались буквы / символы?')

    if len(str(count)) > 10:
        raise Exception('Не думаешь, что этого излишне много?')


# Проверка валидности скрытости товара
async def validate_is_hidden(text):
    if text.casefold() not in map(str.casefold, DICTIONARY_ADD_PRODUCT_IS_HIDDEN_YES):
        if text.casefold() not in map(str.casefold, DICTIONARY_ADD_PRODUCT_IS_HIDDEN_NO):
            raise Exception('Не понимаю, Да или Нет?')
