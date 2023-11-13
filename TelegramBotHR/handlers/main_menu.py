from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from func import menu_func


router = Router()


@router.message(Command("start"))
async def cmd_test(message: Message, state: FSMContext):
    await message.answer(text=f'Добро пожаловать в HR бота')
    await menu_func.start_check(message.answer, message.from_user, state)

