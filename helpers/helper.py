from aiogram.dispatcher import FSMContext
from aiogram import types
from create_bot import bot
from aiogram.types import InlineKeyboardMarkup
from multipledispatch import dispatch


# Удаление inline кнопок у сообщений для типа CallbackQuery
@dispatch(types.CallbackQuery)
async def delete_inline_button_callback(call, state=None):
    try:
        if state is None:
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                message_id=call.message.message_id,
                                                reply_markup=InlineKeyboardMarkup())
        else:
            async with state.proxy() as data:
                await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                    message_id=data['message_id'],
                                                    reply_markup=InlineKeyboardMarkup())
    except Exception as err:
        print(f'message_id - not found - \n{call.message.message_id} - \n{err}')


# Удаление inline кнопок у сообщений для типа message
@dispatch(types.Message, FSMContext)
async def delete_inline_button_message(message, state):
    async with state.proxy() as data:
        try:
            await bot.edit_message_reply_markup(chat_id=message.chat.id,
                                                message_id=data['message_id'],
                                                reply_markup=InlineKeyboardMarkup())
        except Exception as err:
            print(f'message_id - not found \n{message.message_id} - \n{err}')
