from create_bot import bot
from keyboards import admin_kb
from aiogram.dispatcher import FSMContext


async def send_text_state(message, state):
    text_state = await text_by_state(state)
    if text_state != '':
        current_state = await state.get_state()
        if current_state == 'FSMAddProducts:isHidden':
            await bot.send_message(message.from_user.id, text_state, reply_markup=admin_kb.kb_ib_ih_admin_add)
        else:
            await bot.send_message(message.from_user.id, text_state, reply_markup=admin_kb.kb_ib_admin_add)
    else:
        await bot.send_message(message.from_user.id, "Произошла ошибка, как ты нахуй это сделал?")


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
