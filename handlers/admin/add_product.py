from create_bot import bot
from aiogram.dispatcher import FSMContext, filters
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State

from data_base import sqlite_db_admin
from helpers.auth.Auth import Auth
from dictionaries.dictionaries_commands import DICTIONARY_ADD_PRODUCT, DICTIONARY_ADD_PRODUCT_IS_HIDDEN_YES
from helpers import projector
from helpers.helper import delete_inline_button_message, delete_inline_button_callback
from helpers.projector import send_product_admin
from helpers.validate import validate_photo, validate_text, validate_price, validate_count, validate_is_hidden
from keyboards import admin_kb


class FSMAddProducts(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()
    count = State()
    isHidden = State()
    change = State()


async def start_add_product(message: types.Message, state: FSMContext):
    if await Auth.check_access_level(message.from_user.username, message.from_user.id, state, "admin"):
        print(f"start_load_product -\n state: {state}\nmessage: {message}")
        async with state.proxy() as data:
            data['id'] = None
            data['photo'] = None
            data['name'] = None
            data['description'] = None
            data['price'] = None
            data['count'] = None
            data['isHidden'] = None
            data['process'] = 'create'
            data['keyboards'] = 'create'

        await controller_state_add_product(message, state)


async def add_product_photo(message: types.Message, state: FSMContext):
    if await Auth.check_access_level(message.from_user.username, message.from_user.id, state, "admin"):
        print(f"add_product_photo -\n state: {state}\nmessage: {message}")
        try:
            await validate_photo(message)
            async with state.proxy() as data:
                data['photo'] = message.photo[0].file_id
            await controller_state_add_product(message, state)
        except Exception as err:
            await message.reply(err)


async def add_product_name(message: types.Message, state: FSMContext):
    if await Auth.check_access_level(message.from_user.username, message.from_user.id, state, "admin"):
        print(f"add_product_name -\n state: {state}\nmessage: {message}")
        try:
            await validate_text(message.text)
            async with state.proxy() as data:
                data['name'] = message.text
            await controller_state_add_product(message, state)
        except Exception as err:
            await message.reply(err)


async def add_product_description(message: types.Message, state: FSMContext):
    if await Auth.check_access_level(message.from_user.username, message.from_user.id, state, "admin"):
        print(f"add_product_description -\n state: {state}\nmessage: {message}")

        try:
            await validate_text(message.text)
            async with state.proxy() as data:
                data['description'] = message.text
            await controller_state_add_product(message, state)
        except Exception as err:
            await message.reply(err)


async def add_product_price(message: types.Message, state: FSMContext):
    if await Auth.check_access_level(message.from_user.username, message.from_user.id, state, "admin"):
        print(f"add_product_price -\n state: {state}\nmessage: {message}")

        try:
            await validate_price(message.text)
            async with state.proxy() as data:
                data['price'] = message.text
            await controller_state_add_product(message, state)
        except Exception as err:
            await message.reply(err)


async def add_product_count(message: types.Message, state: FSMContext):
    if await Auth.check_access_level(message.from_user.username, message.from_user.id, state, "admin"):
        print(f"add_product_count -\n state: {state}\nmessage: {message}")

        try:
            await validate_count(message.text)
            async with state.proxy() as data:
                data['count'] = message.text

            if int(message.text) == 0:
                async with state.proxy() as data:
                    data['isHidden'] = 1
                    data['id'] = -1
                    await bot.send_message(message.from_user.id,
                                           "Количество товаров = 0\nВидимость автоматически проставлена в 0 (Не виден пользователю)")

            await controller_state_add_product(message, state)
        except Exception as err:
            await message.reply(err)


async def add_product_is_hidden_call(call: types.CallbackQuery, state: FSMContext):
    if await Auth.check_access_level(call.from_user.username, call.from_user.id, state, "admin"):
        print(f"add_product_is_hidden_call -\n state: {state}\nmessage: {call}")

        try:
            call_is_hidden = call.data.replace('is_hidden_', '')
            if call_is_hidden == 'yes':
                is_hidden = 0
            else:
                is_hidden = 1
            async with state.proxy() as data:
                data['isHidden'] = is_hidden
                data['id'] = -1
            await delete_inline_button_callback(call)
            await change_add_product(call.from_user.id, state)
            await call.answer()
        except Exception as err:
            await bot.send_message(call.from_user.id, err)


async def add_product_is_hidden(message: types.Message, state: FSMContext):
    if await Auth.check_access_level(message.from_user.username, message.from_user.id, state, "admin"):
        print(f"add_product_is_hidden -\n state: {state}\nmessage: {message}")

        try:
            await validate_is_hidden(message.text)
            if message.text in DICTIONARY_ADD_PRODUCT_IS_HIDDEN_YES:
                is_hidden = 1
            else:
                is_hidden = 0

            async with state.proxy() as data:
                data['isHidden'] = is_hidden
                data['id'] = -1

            await delete_inline_button_message(message, state)
            await change_add_product(message.from_user.id, state)
        except Exception as err:
            await message.reply(err)


async def change_add_product(chat_id, state: FSMContext):
    async with state.proxy() as data:
        data['keyboards'] = 'edit'
        await FSMAddProducts.change.set()
        await send_product_admin(chat_id, data['photo'], data['name'], data['description'],
                                 data['price'], data['count'], data['isHidden'], data['process'])


async def controller_state_add_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        id_p = data['id']
        keyboard = data['keyboards']
    await delete_inline_button_message(message, state)
    if id_p is None:
        if state is None:
            await FSMAddProducts.photo.set()
        else:
            await FSMAddProducts.next()

        msg = await projector.send_text_state(message.from_user.id, state, keyboard)
        async with state.proxy() as data:
            data['message_id'] = msg.message_id
    else:
        await FSMAddProducts.change.set()
        await change_add_product(message.from_user.id, state)


async def controller_state_edit_product(call: types.CallbackQuery, state: FSMContext):
    if await Auth.check_access_level(call.from_user.username, call.from_user.id, state, "admin"):
        await delete_inline_button_callback(call)

        edit_code = call.data.replace('edit_', '')
        if edit_code == 'photo':
            await FSMAddProducts.photo.set()
        if edit_code == 'name':
            await FSMAddProducts.name.set()
        if edit_code == 'description':
            await FSMAddProducts.description.set()
        if edit_code == 'price':
            await FSMAddProducts.price.set()
        if edit_code == 'count':
            await FSMAddProducts.count.set()
        if edit_code == 'is_hidden':
            await FSMAddProducts.isHidden.set()

        if edit_code == 'cancel':
            await state.finish()
            await bot.send_message(call.from_user.id, 'Операция отменена',
                                   reply_markup=admin_kb.kb_admin_global)
        elif edit_code == 'save':
            await add_product_finish(call, state)
        else:
            async with state.proxy() as data:
                keyboard = data['keyboards']
            msg = await projector.send_text_state(call.from_user.id, state, keyboard)
            async with state.proxy() as data:
                data['message_id'] = msg.message_id

        await call.answer()


async def prev_callback_add_product(call: types.CallbackQuery, state: FSMContext):
    if await Auth.check_access_level(call.from_user.username, call.from_user.id, state, "admin"):
        print(f"prev_callback_add_product -\n state: {state}\nmessage: {call}")
        current_state = await state.get_state()
        print(current_state)
        async with state.proxy() as data:
            keyboard = data['keyboards']
        if keyboard == 'edit':
            await delete_inline_button_callback(call)
            await change_add_product(call.from_user.id, state)
            await call.answer()
            return

        if current_state == 'FSMAddProducts:photo':
            await delete_inline_button_callback(call)
            await cancel_callback_add_product(call, state)
            await call.answer()
            return

        await delete_inline_button_callback(call)
        await FSMAddProducts.previous()
        await call.answer('Вернулись на шаг назад')
        msg = await projector.send_text_state(call.from_user.id, state, keyboard)
        async with state.proxy() as data:
            data['message_id'] = msg.message_id


async def cancel_callback_add_product(call: types.CallbackQuery, state: FSMContext):
    if await Auth.check_access_level(call.from_user.username, call.from_user.id, state, "admin"):
        print(f"cancel_callback_add_product -\n state: {state}\nmessage: {call}")
        await delete_inline_button_callback(call)
        await state.finish()
        await bot.send_message(call.from_user.id, 'Операция отменена',
                               reply_markup=admin_kb.kb_admin_global)


async def add_product_finish(call: types.CallbackQuery, state: FSMContext):
    if await Auth.check_access_level(call.from_user.username, call.from_user.id, state, "admin"):
        async with state.proxy() as data:
            await sqlite_db_admin.add_product_catalog(state)
            await bot.send_message(call.from_user.id, f"Продукт успешно добавлен -\n{data}",
                                   reply_markup=admin_kb.kb_admin_global)
            await state.finish()


def register_handlers_admin_add(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_callback_add_product, lambda x: x.data and x.data.startswith('cancel'),
                                       state="*")
    dp.register_callback_query_handler(prev_callback_add_product, lambda x: x.data and x.data.startswith('previous'),
                                       state="*")

    dp.register_message_handler(start_add_product, filters.Text(endswith=DICTIONARY_ADD_PRODUCT, ignore_case=True),
                                state=None)
    dp.register_message_handler(add_product_photo, content_types=['text', 'photo'], state=FSMAddProducts.photo)
    dp.register_message_handler(add_product_name, state=FSMAddProducts.name)
    dp.register_message_handler(add_product_description, state=FSMAddProducts.description)
    dp.register_message_handler(add_product_price, state=FSMAddProducts.price)
    dp.register_message_handler(add_product_count, state=FSMAddProducts.count)
    dp.register_message_handler(add_product_is_hidden, state=FSMAddProducts.isHidden)
    dp.register_callback_query_handler(add_product_is_hidden_call,
                                       filters.Text(startswith='is_hidden', ignore_case=True),
                                       state=FSMAddProducts.isHidden)

    dp.register_callback_query_handler(controller_state_edit_product, lambda x: x.data and x.data.startswith('edit_'),
                                       state=FSMAddProducts.change)
