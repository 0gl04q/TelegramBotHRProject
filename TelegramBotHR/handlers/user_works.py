from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from func import menu_func
from filters import UserRoleFilter, CheckSurveysFilter, ChangeLanguageFilter
from states import MenuStates
from keyboards.for_menu import keyboard_list
import db
import languages.languages as lg

router = Router()


@router.message(CheckSurveysFilter(), UserRoleFilter())
async def check_tests(message: Message, state: FSMContext):
    await menu_func.start_check(message.answer, message.from_user, state)


@router.message(ChangeLanguageFilter(), UserRoleFilter())
async def change_language(message: Message, state: FSMContext):
    language = db.get_language(message.from_user.id)

    language_data = lg.get_languages_data()

    all_languages = db.get_all_languages()

    await message.answer(
        text=language_data[language]['UserWorks']['Keyboards']['QuestSelectLanguage'],
        reply_markup=keyboard_list(all_languages, key='lang')
    )
    await state.set_state(MenuStates.choosing_language)


@router.callback_query(MenuStates.choosing_language, F.data.startswith("lang_"))
async def add_test_user(callback: CallbackQuery, state: FSMContext):
    language_id = callback.data.split("_")[1]

    db.update_language(callback.from_user.id, language_id)

    language = db.get_language(callback.from_user.id)

    language_data = lg.get_languages_data()

    await callback.message.edit_text(text=language_data[language]['UserWorks']['Keyboards']['LanguageChanged'])
    await menu_func.start_check(callback.message.answer, callback.from_user, state)
