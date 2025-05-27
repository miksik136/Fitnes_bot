import datetime
import traceback

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils import keyboard

from db.models import Days, Users
from db.repository import users_repository, admins_repository
from settings import start_keyboard, InputMessage, answ_keyboard
from utils.gpt_api import API_GPT
from utils.check_time import time_or_no

user_router = Router()


@user_router.message(F.text == '/start')
async def on_start(message: Message):
    await message.answer('choose move', reply_markup=start_keyboard.as_markup())


@user_router.callback_query(F.data == 'retime')
async def on_retime(call: CallbackQuery, state: FSMContext):
    await call.message.answer(text='enter time in formate "number:number"')
    await state.set_state(InputMessage.enter_time)

@user_router.message(F.text, InputMessage.enter_time)
async def on_edit_time(message: Message, state: FSMContext):
    text = message.text
    integ = text.split(':')
    user_id = message.from_user.id
    if time_or_no(text) is True:
        await users_repository.update_time_notification_by_user_id(user_id=user_id,
                                                                   new_time=datetime.time(hour=int(integ[0]),
                                                                                          minute=int(integ[1])))
        await message.answer('time added')
    else:
        await message.answer(text='it is not time')
    await state.clear()


@user_router.callback_query(F.data == 'connect')
async def on_connect(call: CallbackQuery, state: FSMContext):
    await call.message.answer(text='enter question for creater')
    await state.set_state(InputMessage.enter_question)


@user_router.message(F.text, InputMessage.enter_question)
async def on_enter_question(message: Message, state: FSMContext, bot: Bot):
    question = message.text
    admins = await admins_repository.select_all_admins()
    user_id = message.from_user.id
    keyboard = answ_keyboard(user_id)
    for admin in admins:
        try:
            admin_id = admin.admin_id
            await bot.send_message(chat_id=admin_id, text=question, reply_markup=keyboard.as_markup())
        except:
            print(traceback.format_exc())
            continue
    await state.clear()


@user_router.callback_query(F.data.startswith('answer|'))
async def on_answer(call: CallbackQuery, state: FSMContext, bot:Bot):
    call_data = call.data.split("|")
    user_id = int(call_data[1])
    await call.message.answer(text="Введи ответ брателла")
    await state.set_state(InputMessage.enter_answer)
    await state.update_data(user_id=user_id)


@user_router.message(F.text, InputMessage.enter_answer)
async def on_enter_answer(message: Message, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    user_id = state_data['user_id']
    text = message.text
    try:
        await bot.send_message(chat_id=user_id, text=text)
        await message.answer(text='user get answer')
    except:
        await message.answer(text='error user not get answer')
    await state.clear()


@user_router.message(F.text == '/a')
async def on_enter_a(message: Message):
    await message.answer('какой?')


@user_router.message(F.text)
async def get_question_to_ai(message: Message):
    question = message.text
    user_id = message.from_user.id
    username = message.from_user.username
    user = await users_repository.get_user_by_user_id(user_id=user_id)
    if user is None:
        user = await users_repository.add_user(user_id=user_id, username=username)
        Days.number_day = 0
        await message.answer('hello')
        return
    thread_id = user.ai_thread_id
    answer = await API_GPT(thread_id).send_message(user_id=user_id, text=question, image_bytes=None)
    if answer is None:
        await message.answer('you not enter question')
    else:
        await message.answer(answer)


#@user_router.message(F.data == 'state')
#async def calories(message: Message):
