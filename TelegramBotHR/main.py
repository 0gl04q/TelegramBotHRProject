import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import main_menu, tests, hr_work, user_works
from db import first_query

import os
from dotenv import load_dotenv

'''
    Основной файл бота
'''

# Функция инициализации переменных окружения из .env
load_dotenv()

logging.basicConfig(level=logging.INFO)

bot_token = os.getenv("BOT_TOKEN")

bot = Bot(token=bot_token, parse_mode="HTML")


async def main():

    first_query()

    dp = Dispatcher(storage=MemoryStorage())

    # Добавление роутов
    dp.include_routers(main_menu.router, tests.router, hr_work.router, user_works.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
