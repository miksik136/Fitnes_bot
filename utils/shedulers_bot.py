import datetime

from aiogram import Bot

from db.repository import users_repository, days_repository


async def send_notification(bot: Bot):
   users = await users_repository.select_all_users()
   now_datetime = datetime.datetime.now()
   now_time = now_datetime.time()
   for user in users:
       try:
           time_notification = user.time_notification
           if time_notification.hour == now_time.hour and time_notification.minute == now_time.minute:
               user_days = await days_repository.get_all_days_user_id(user_id=user.user_id)
               last_day_number = max([day.number_day for day in user_days])
               day_obj = await days_repository.get_all_day_by_number(number=last_day_number, user_id=user.user_id)
               calories_day = day_obj.total_calories
               if calories_day == 0:
                   text = "Ты сегодня не похавал"
               else:
                    text = f'you get calories: {calories_day}'
               await bot.send_message(text=text, chat_id=user.user_id)

       except:
            continue