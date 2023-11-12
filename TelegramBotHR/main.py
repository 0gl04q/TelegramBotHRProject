import asyncio
import logging
import config
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import main_menu, tests, hr_work
from db import first_query

import os
from dotenv import load_dotenv

'''
    Основной файл бота
'''

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot_token = os.getenv("BOT_TOKEN")

bot = Bot(token=bot_token, parse_mode="HTML")


async def main():
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(main_menu.router, tests.router, hr_work.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
