from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from func import menu_func
from filters import UserRoleFilter
from states import MenuStates
from keyboards.for_menu import keyboard_list
import db
from translators import translate_text

router = Router()


@router.message(Command("start"))
async def cmd_test(message: Message, state: FSMContext):
    await message.answer(text=f'Добро пожаловать в HR бота')
    await menu_func.start_check(message.answer, message.from_user, state)


@router.message(F.text.in_(['Проверить наличие опросов', 'View survey availability']), UserRoleFilter())
async def check_tests(message: Message, state: FSMContext):
    await menu_func.start_check(message.answer, message.from_user, state)


@router.message(F.text.in_(['Выбрать язык', 'Select language']), UserRoleFilter())
async def change_language(message: Message, state: FSMContext):
    language = db.get_language(message.from_user.id)

    all_languages = db.get_all_languages()

    await message.answer(
        text=translate_text('Выберите язык', to_language=language),
        reply_markup=keyboard_list(all_languages, key='lang')
    )
    await state.set_state(MenuStates.choosing_language)


@router.callback_query(MenuStates.choosing_language, F.data.startswith("lang_"))
async def add_test_user(callback: CallbackQuery, state: FSMContext):

    language_id = callback.data.split("_")[1]

    db.update_language(callback.from_user.id, language_id)

    language = db.get_language(callback.from_user.id)

    await callback.message.edit_text(text=translate_text('Язык успешно изменен', to_language=language), src='ru', dest=language)
    await menu_func.start_check(callback.message.answer, callback.from_user, state)

