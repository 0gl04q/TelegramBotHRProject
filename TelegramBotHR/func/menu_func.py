from keyboards.for_menu import keyboard_menu_user, keyboard_list, keyboard_menu_HR
from states import MenuStates
import db
from translators import translate_text


async def change_tests(available_tests_tl, answer, state, user_id, language):
    await answer(
        text=translate_text("Ищем опросы...", to_language=language),
        reply_markup=keyboard_menu_user(language)
    )
    if available_tests_tl:
        await answer(
            text=translate_text("Выберите опрос:", to_language=language),
            reply_markup=keyboard_list(available_tests_tl, key='t')
        )

        await state.update_data(user_id=user_id)
        await state.set_state(MenuStates.choosing_test)
    else:
        await answer(text=translate_text("У вас пока нет активных опросов", to_language=language), reply_markup=keyboard_menu_user(language))


async def start_check(answer, from_user, state):
    info_user = db.get_user_by_id(from_user.id)

    if info_user:
        user_id, name, role, status = info_user

        tg_id = from_user.id

        language = db.get_language(tg_id)

        if status:
            if role == 0:
                await answer(text="Меню HR:", reply_markup=keyboard_menu_HR())
                await state.set_state(MenuStates.choosing_test)
            elif role == 1:

                available_tests_tl = db.get_user_tests(user_id)

                if available_tests_tl:
                    available_tests_tl = [(test[0], translate_text(test[1], to_language=language)) for test in available_tests_tl]

                await change_tests(available_tests_tl, answer, state, user_id, language)

        else:
            await answer(text=translate_text('Ваш пользователь заблокирован', to_language=language))
    else:
        await answer(text='Спасибо за подключение бота, ожидайте пока HR добавит вас')