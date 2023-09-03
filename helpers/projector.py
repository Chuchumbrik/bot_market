from create_bot import bot
from keyboards import admin_kb
from aiogram.dispatcher import FSMContext


async def send_text_state(chat_id, state, keyboard=None):
    text_state = await text_by_state(state)
    if text_state != '':
        current_state = await state.get_state()
        if keyboard == 'create':
            if current_state == 'FSMAddProducts:isHidden':
                return await bot.send_message(chat_id, text_state, reply_markup=admin_kb.kb_ib_ih_admin_add)
            else:
                return await bot.send_message(chat_id, text_state, reply_markup=admin_kb.kb_ib_admin_add)
        elif keyboard == 'edit':
            if current_state == 'FSMAddProducts:isHidden':
                return await bot.send_message(chat_id, text_state, reply_markup=admin_kb.kb_ib_ih_admin_edit)
            else:
                return await bot.send_message(chat_id, text_state, reply_markup=admin_kb.kb_ib_admin_edit)
    else:
        return await bot.send_message(chat_id, "Произошла ошибка, как ты нахуй это сделал?")


async def text_by_state(state: FSMContext):
    current_state = await state.get_state()
    text_state = ''
    print(current_state)

    unit_to_multiplier = {
        'FSMAddProducts:photo': 'Загрузи фото',
        'FSMAddProducts:name': 'Теперь название продукта',
        'FSMAddProducts:description': 'Теперь описание продукта',
        'FSMAddProducts:price': 'Теперь цену продукта',
        'FSMAddProducts:count': 'Количество товара?',
        'FSMAddProducts:isHidden': 'Мы хотим показать это сейчас пользователям?',
    }

    try:
        text_state = unit_to_multiplier[current_state]
    except KeyError as e:
        print('Undefined unit: {}'.format(e.args[0]))

    return text_state


async def send_product_admin(chat_id, p_photo, p_name, p_description, p_price, p_count, p_hidden, keyboard=None):
    p_hidden = "Продукт не виден клиентам" if p_hidden else "Продукт виден клиентам"
    if keyboard is None:
        message = await bot.send_photo(chat_id, p_photo,
                                       f'Название: {p_name}\n'
                                       f'Описание: {p_description}\n'
                                       f'Цена: {p_price} рупи\n'
                                       f'Количество: {p_count}\n'
                                       f'Видимость: {p_hidden}')

    if keyboard == 'edit':
        message = await bot.send_photo(chat_id, p_photo,
                                       f'Название: {p_name}\n'
                                       f'Описание: {p_description}\n'
                                       f'Цена: {p_price} рупи\n'
                                       f'Количество: {p_count}\n'
                                       f'Видимость: {p_hidden}',
                                       reply_markup=admin_kb.kb_admin_edit)

    if keyboard == 'create':
        message = await bot.send_photo(chat_id, p_photo,
                                       f'Название: {p_name}\n'
                                       f'Описание: {p_description}\n'
                                       f'Цена: {p_price} рупи\n'
                                       f'Количество: {p_count}\n'
                                       f'Видимость: {p_hidden}',
                                       reply_markup=admin_kb.kb_ib_admin_add_edit)
    return message


async def send_product_client(chat_id, p_photo, p_name, p_description, p_price, p_count):
    return await bot.send_photo(chat_id, p_photo,
                                f'Название: {p_name}\n'
                                f'Описание: {p_description}\n'
                                f'Цена: {p_price} рупи\n'
                                f'Количество: {p_count}')
