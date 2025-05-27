import re
from os import getenv

from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

from db.repository import users_repository, ai_requests_repository

load_dotenv(find_dotenv('../.env'))
api_key = getenv('GPT_TOKEN')
assistant_id = getenv('ASSISTANT_ID')

class API_GPT:
    def __init__(self, thread_id: str| None):
        self.client = OpenAI(api_key=api_key)
        self.assistant = self.client.beta.assistants.retrieve(assistant_id=assistant_id)
        self.thread_id = thread_id

    async def update_thread_id(self,user_id: int):
        thread = self.client.beta.threads.create()
        self.thread_id = thread.id
        await users_repository.update_thread_id_by_user_id(user_id=user_id, thread_id=self.thread_id)
        return thread

    async def send_message(self,user_id, text: str | None, image_bytes=None):
        if self.thread_id is None:
            thread = await self.update_thread_id(user_id=user_id)
        else:
            thread = self.client.beta.threads.retrieve(thread_id=self.thread_id)
        if text is None and image_bytes is None:
            return None
        elif image_bytes is None:
            content = text
        else:
            if text is None:
                text = 'it is your image'
            image_bytes.seek(0)
            user_file = self.client.files.create(file=('image.png', image_bytes), purpose='vision')
            content = [{'type': 'text', 'text': text}, {'type': 'image_file', 'image_file': {'file_id': user_file.id}}]
        thread_message = self.client.beta.threads.messages.create(thread_id=self.thread_id, role='user', content=content)
        run = self.client.beta.threads.runs.create_and_poll(thread_id=self.thread_id, assistant_id=self.assistant.id)
        if run.status == 'completed':
            messages = self.client.beta.threads.messages.list(thread_id=self.thread_id)
            return messages.data[0].content[0].text.value.replace('**', '').replace('#', '')

        async def enter_ai_question(message: Message):
            user = await users_repository.get_user_by_user_id(message.from_user.id)
            thread_id = user.ai_thread_id
            answer = await API_GPT(thread_id=thread_id).send_message(text=message.text, user_id=message.from_user.id)
            try:
                pattern = re.compile(r'Итого за данный прием пищи: \$\d+(\.\d+)?\$ калорий')
                if re.search(pattern, answer):
                    calories = answer.split('\n')[-1].split('$')[-2]
                    keyboard = InlineKeyboardBuilder()
                    keyboard.row(InlineKeyboardButton(text='внести в свой рацион', callback_data=f'enter_calories|{float(calories)}'))
                    await message.reply(text=answer.replace('$', ''), reply_markup=keyboard.as_markup())
                else:
                    await message.reply(text=answer.replace('$', ''))
            except:
                await message.reply(text=answer.replace('$', ''))
            finally:
                await ai_requests_repository.add_request(user_id=message.from_user.id, user_question=message.text, ai_answer=answer)







