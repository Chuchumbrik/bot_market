from create_bot import bot
from aiogram.dispatcher import FSMContext, filters
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from helpers.auth.Auth import Auth
from dictionaries.dictionaries_commands import DICTIONARY_ADD_PRODUCT
from helpers import projector
from helpers.helper import delete_inline_button_message
from helpers.validate import validate_photo, validate_text, validate_price, validate_count, validate_is_hidden
from keyboards import admin_kb



class FSMAddProducts(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()
    count = State()
    isHidden = State()


async def start_add_product(message: types.Message, state: FSMContext):
    if await Auth.check_access_level(message.from_user.username, message.from_user.id, state, "admin"):
        print(f"start_load_product -\n state: {state}\nmessage: {message}")
        async with state.proxy() as data:
            data['id'] = -2
            data['photo'] = -2
            data['name'] = -2
            data['description'] = -2
            data['price'] = -2
            data['count'] = -2
            data['isHidden'] = -2

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
            await controller_state_add_product(message, state)
        except Exception as err:
            await message.reply(err)


async def add_product_is_hidden_call(call: types.CallbackQuery, state: FSMContext):
    if await Auth.check_access_level(call.from_user.username, call.from_user.id, state, "admin"):
        print(f"add_product_is_hidden -\n state: {state}\nmessage: {call}")

        try:
            call_is_hidden = call.data.replace('is_hidden_', '')
            if call_is_hidden == 'yes':
                is_hidden = 0
            else:
                is_hidden = 1
            async with state.proxy() as data:
                data['isHidden'] = is_hidden
            await add_product_finish(state, call.from_user.id)
            await call.answer()
        except Exception as err:
            await bot.send_message(call.from_user.id, err)


async def add_product_is_hidden(message: types.Message, state: FSMContext):
    if await Auth.check_access_level(message.from_user.username, message.from_user.id, state, "admin"):
        print(f"add_product_is_hidden -\n state: {state}\nmessage: {message}")

        try:
            await validate_is_hidden(message.text)
            await add_product_finish(state, message.chat.id)
        except Exception as err:
            await message.reply(err)


async def add_product_finish(state: FSMContext, chat_id):

    async with state.proxy() as data:
        await bot.send_message(chat_id, f"Продукт успешно добавлен -\n{data}", reply_markup=admin_kb.kb_admin_global)
    await state.finish()


async def controller_state_add_product(message: types.Message, state: FSMContext):
    if state is None:
        await FSMAddProducts.photo.set()
    else:
        await FSMAddProducts.next()

    msg = await projector.send_text_state(message, state)
    async with state.proxy() as data:
        data['message_id'] = msg


async def prev_callback_add_product(call: types.CallbackQuery, state: FSMContext):
    if await Auth.check_access_level(call.from_user.username, call.from_user.id, state, "admin"):
        print(f"prev_callback_add_product -\n state: {state}\nmessage: {call}")
        current_state = await state.get_state()
        if current_state == 'FSMAddProducts:photo':
            await cancel_callback_add_product(call, state)
            await call.answer()
            return
        await delete_inline_button_message(call, state)
        await FSMAddProducts.previous()
        await call.answer('Вернулись на шаг назад')


async def cancel_callback_add_product(call: types.CallbackQuery, state: FSMContext):
    if await Auth.check_access_level(call.from_user.username, call.from_user.id, state, "admin"):
        print(f"cancel_callback_add_product -\n state: {state}\nmessage: {call}")
        await delete_inline_button_message(call, state)
        await state.finish()
        await bot.send_message(call.from_user.id, 'Операция отменена',
                               reply_markup=admin_kb.kb_admin_global)


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
    dp.register_callback_query_handler(add_product_is_hidden_call, filters.Text(startswith='is_hidden', ignore_case=True),
                                state=FSMAddProducts.isHidden)
