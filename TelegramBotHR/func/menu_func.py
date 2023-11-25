from keyboards.for_menu import keyboard_menu_user, keyboard_list, keyboard_menu_HR
from states import MenuStates
import db
import languages.languages as lg


async def change_tests(available_tests_tl, answer, state, user_id, language_data, role=0):

    await answer(
        text=language_data['UserWorks']['Keyboards']['LookingSurveys'],
        reply_markup=keyboard_menu_user(language_data) if role else None
    )

    if available_tests_tl:
        await answer(
            text=language_data['UserWorks']['Keyboards']['SelectSurvey'],
            reply_markup=keyboard_list(available_tests_tl, key='t')
        )

        await state.update_data(user_id=user_id)
        await state.set_state(MenuStates.choosing_test)
    else:
        await answer(
            text=language_data['UserWorks']['Keyboards']['NoSurvey'],
            reply_markup=keyboard_menu_user(language_data) if role else None
        )


async def start_check(answer, from_user, state):

    # ищем информацию о пользователе
    info_user = db.get_user_by_id(from_user.id)

    if info_user:
        user_id, name, role, status = info_user

        tg_id = from_user.id

        language = db.get_language(tg_id)
        language_data = lg.get_languages_data()[language]

        available_tests_tl = db.get_user_tests(user_id, language)
        if status:
            if role == 0:
                await answer(text="Меню HR:", reply_markup=keyboard_menu_HR())
                await state.set_state(MenuStates.choosing_test)
                await change_tests(available_tests_tl, answer, state, user_id, language_data, role)
            elif role == 1:
                await change_tests(available_tests_tl, answer, state, user_id, language_data, role)

        else:
            await answer(text=language_data['UserWorks']['Main']['Blocked'])
    else:
        await answer(text='Спасибо за подключение, ожидайте пока HR добавит вас')
