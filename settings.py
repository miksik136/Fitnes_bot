from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import Admins
from db.repository import AdminsRepository

storage_bot = MemoryStorage()
storage_admin_bot = MemoryStorage()

async def generate_list():
    admins = await AdminsRepository().select_all_admins()
    keyboard = InlineKeyboardBuilder()
    for admin in admins:
        keyboard.row(InlineKeyboardButton(text=f"{admin.username}", callback_data=f'admin|{admin.admin_id}'))
    keyboard.row(InlineKeyboardButton(text='отмена', callback_data='cancel_key'))
    return keyboard

async def confirm_delete_admin(admin_id):
    yes_no_keyboard = InlineKeyboardBuilder()
    yes_no_keyboard.row(InlineKeyboardButton(text='YES', callback_data=f'yes|{admin_id}'))
    yes_no_keyboard.row(InlineKeyboardButton(text='NO', callback_data='cancel'))
    return yes_no_keyboard

admin_keyboard = InlineKeyboardBuilder()
admin_keyboard.row(InlineKeyboardButton(text="статистика", callback_data='stat_admin'))
admin_keyboard.row(InlineKeyboardButton(text='добавить/удалить админа', callback_data='add_del_admin'))
admin_keyboard.row(InlineKeyboardButton(text='сделать рассылку', callback_data='mail_admin'))

add_del_keyboard = InlineKeyboardBuilder()
add_del_keyboard.row(InlineKeyboardButton(text='добавить', callback_data='add_admin'))
add_del_keyboard.row(InlineKeyboardButton(text='удалить', callback_data='del_admin'))

ot_keyboard = InlineKeyboardBuilder()
ot_keyboard.row(InlineKeyboardButton(text='отмена', callback_data='cancel_key'))

start_keyboard = InlineKeyboardBuilder()
start_keyboard.row(InlineKeyboardButton(text='статистика на сегодня', callback_data='state'))
start_keyboard.row(InlineKeyboardButton(text='изменить время отправляемого отчёта', callback_data='retime'))
start_keyboard.row(InlineKeyboardButton(text='связь с разработчиком', callback_data='connect'))

def answ_keyboard(user_id:int):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='answer', callback_data=f'answer|{user_id}'))
    return keyboard

class InputMessage(StatesGroup):
    enter_time = State()
    enter_id = State()
    enter_question = State()
    enter_answer = State()

