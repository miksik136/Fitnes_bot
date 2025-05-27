import asyncio

from aiogram import Bot, Dispatcher

from db.engine import DatabaseEngine
from handlerses.admin_handlers import admin_router
from settings import storage_admin_bot

token = '8182373482:AAFAODwNoWT8evEMlhW4C22g_wbH7gbjQIU'
main_admin_bot = Bot(token=token)


async def main():
    db_engine = DatabaseEngine()
    await db_engine.proceed_schemas()
    print(await main_admin_bot.get_me())
    dp = Dispatcher(storage=storage_admin_bot)
    dp.include_routers(admin_router)
    await dp.start_polling(main_admin_bot)

asyncio.run(main())