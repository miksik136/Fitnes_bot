from aiogram import Router, F, types, Bot
from aiogram.client import bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db.models import Admins
from db.repository import admins_repository
from settings import admin_keyboard, add_del_keyboard, InputMessage, ot_keyboard, generate_list, confirm_delete_admin

admin_router = Router()

@admin_router.message(F.text == '/admin')
async def admin_message(message: Message):
    await message.answer('Привет, можешь выбрать следующее действие', reply_markup=admin_keyboard.as_markup())

@admin_router.callback_query(F.data == 'add_del_admin')
async def add_del_admin(call: types.CallbackQuery):
    await call.message.edit_text('что ты хочешь сделать?', reply_markup=add_del_keyboard.as_markup())

@admin_router.callback_query(F.data == 'add_admin')
async def add_admin(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('enter admin id', reply_markup=ot_keyboard.as_markup())
    await state.set_state(InputMessage.enter_id)

@admin_router.callback_query(F.data == 'cancel_key')
async def cancel_button(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete()
    await call.message.answer('Привет, можешь выбрать следующее действие', reply_markup=admin_keyboard.as_markup())

@admin_router.message(F.text, InputMessage.enter_id)
async def add_with_id(message: Message, state: FSMContext, bot: Bot):
    admin_id = message.text
    try:
        message2 = await bot.send_message(chat_id=admin_id, text='you add in admin')
        await state.clear()
        await admins_repository.add_admin(admin_id=admin_id, username=message2.chat.username)
        await message.answer('admin successfully added')
    except:
         await message.answer('user not found or he added, try enter id again')

@admin_router.callback_query(F.data == 'del_admin')
async def del_admin(call: types.CallbackQuery):
    keyboard = await generate_list()
    await call.message.edit_text('Good now choose admin', reply_markup=keyboard.as_markup())

@admin_router.callback_query(F.data.startswith('admin|'))
async def yes_no_delete(call: types.CallbackQuery):
    data = call.data.split('|')
    keyboard = await confirm_delete_admin(data[1])
    await call.message.edit_text('you want delete admin?', reply_markup=keyboard.as_markup())

@admin_router.callback_query(F.data.startswith('yes|'))
async def delete_admin(call: types.CallbackQuery):
    data = call.data.split('|')
    admin_id = data[1]
    await admins_repository.delete_admin_by_admin_id(admin_id)
    await call.message.answer('admin successfully deleted')

@admin_router.callback_query(F.data == 'cancel')
async def cencel_move(call: types.CallbackQuery):
    keyboard = await generate_list()
    await call.message.delete()
    await call.message.answer('Good now choose admin', reply_markup=keyboard.as_markup())