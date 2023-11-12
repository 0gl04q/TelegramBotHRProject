from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from func import menu_func
import db
from aiogram import types
from states import MenuStates, TestStates
from keyboards.for_test import yes_no_kb, zero_to_nine
from db import get_questions
from translators import translate_text

router = Router()


async def update_text(message: types.Message, tg_id, question: str, q_number: int):
    language = db.get_language(tg_id)
    await message.edit_text(
        translate_text(question, to_language=language),
        reply_markup=yes_no_kb(language)
    )


@router.callback_query(MenuStates.choosing_test, F.data.startswith("t_"))
async def test_chosen(callback: types.CallbackQuery, state: FSMContext):
    test_id = callback.data.split("_")[1]

    type_id = db.get_type_test(test_id)[0]

    language = db.get_language(callback.from_user.id)

    match type_id:
        case 0:
            q12 = get_questions(test_id)

            await state.update_data(questions=q12, number_question=0, total=0, test_id=test_id)

            first_question = q12[0][0]

            await callback.message.edit_text(translate_text(first_question, to_language=language), reply_markup=yes_no_kb(language))

        case 1:
            enps = get_questions(test_id)

            await state.update_data(questions=enps, number_question=0, total=0, test_id=test_id)

            first_question = enps[0][0]

            await callback.message.edit_text(translate_text(first_question, to_language=language), reply_markup=zero_to_nine())

    await state.set_state(TestStates.passing_test)


@router.callback_query(TestStates.passing_test, F.data.startswith("zn_"))
async def callbacks_enps(callback: types.CallbackQuery, state: FSMContext):
    user_value = await state.get_data()

    language = db.get_language(callback.from_user.id)

    total = int(callback.data.split("_")[1])

    await callback.message.edit_text(translate_text(f"Итого: {total} баллов", to_language=language))

    db.update_result(test_id=user_value['test_id'], user_id=user_value['user_id'], result=total)

    await menu_func.start_check(callback.message.answer, callback.from_user, state)


@router.callback_query(TestStates.passing_test, F.data.startswith("yn_"))
async def callbacks_q12(callback: types.CallbackQuery, state: FSMContext):
    user_value = await state.get_data()

    language = db.get_language(callback.from_user.id)

    action = callback.data.split("_")[1]

    if action == "yes":
        user_value['number_question'] += 1
        user_value['total'] += 1

    elif action == "no":
        user_value['number_question'] += 1

    if user_value['number_question'] < 12:
        await update_text(
            callback.message,
            callback.from_user.id,
            user_value['questions'][user_value['number_question']][0],
            user_value['number_question']
        )
        await state.update_data(**user_value)
    else:
        await callback.message.edit_text(translate_text(f"Итого: {user_value['total']} баллов", to_language=language))

        db.update_result(test_id=user_value['test_id'], user_id=user_value['user_id'], result=user_value['total'])

        await menu_func.start_check(callback.message.answer, callback.from_user, state)
