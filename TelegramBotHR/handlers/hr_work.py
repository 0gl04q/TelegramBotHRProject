from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import db
from keyboards.for_menu import keyboard_list, keyboard_menu_user
from filters import AdminRoleFilter
from states import AddTestUser, MenuStates, UpdateRoleUser, ReportStates
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value
)
from main import bot
import languages.languages as lg

router = Router()


@router.callback_query(AddTestUser.choosing_test, F.data.startswith("at_"))
async def add_test_user(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    tg_id = user_data['tg_id']
    test_id = callback.data.split("_")[1]

    if db.check_test_result_user(tg_id, test_id):
        await callback.message.edit_text(text='Этот опрос уже добавлен пользователю')
    else:
        db.add_test_result_user(tg_id, test_id)
        await callback.message.edit_text(text='Опрос успешно добавлен пользователю')
    await state.set_state(MenuStates.choosing_action)


@router.callback_query(UpdateRoleUser.update_role, F.data.startswith("cr_"))
async def update_role_user(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    tg_id = user_data['tg_id']
    role_id = callback.data.split("_")[1]

    db.update_role_user(tg_id, role_id)
    await callback.message.edit_text(text='Роль пользователю установлена')
    await state.set_state(MenuStates.choosing_action)


@router.callback_query(ReportStates.choosing_test, F.data.startswith("gt_"))
async def get_report_test(callback: CallbackQuery, state: FSMContext):
    test_id = callback.data.split("_")[1]

    all_users_test = db.get_results_tests(test_id)
    success = db.get_results_tests_success(test_id)
    no_success = db.get_results_tests_no_success(test_id)

    content = as_list(
        as_marked_section(
            Bold("Прошли:"),
            *(success if success else ['Никто']),
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Не прошли:"),
            *(no_success if no_success else ['Никто']),
            marker="❌ ",
        ),
        as_marked_section(
            Bold("Итого:"),
            as_key_value("Всего", len(all_users_test)),
            as_key_value("Прошли", len(success)),
            as_key_value("Не прошли", len(no_success)),
            marker="- ",
        ),
        sep="\n\n",
    )

    await callback.message.edit_text(**content.as_kwargs())
    await state.set_state(MenuStates.choosing_action)


@router.message(F.user_shared, AdminRoleFilter())
async def get_shared_user(message: Message, state: FSMContext):
    user_in_db = db.get_user_by_id(tg_id=message.user_shared.user_id)

    # Дефолтный язык русский
    language_data = lg.get_languages_data()['ru']

    # Добавление пользователя
    if message.user_shared.request_id == 1:
        if not user_in_db:
            await add_user(message, user_in_db)
            await state.set_state(MenuStates.choosing_action)
            await bot.send_message(
                chat_id=message.user_shared.user_id,
                text='Вас добавили в HR бота!',
                reply_markup=keyboard_menu_user(language_data)
            )
        else:
            await message.answer(text='Пользователь уже добавлен в бота')

    # Назначение теста пользователю
    elif message.user_shared.request_id == 2:
        if user_in_db:
            all_test = db.get_all_tests()
            await state.update_data(tg_id=message.user_shared.user_id)
            await state.set_state(AddTestUser.choosing_test)
            await message.answer(text='Выберите опрос', reply_markup=keyboard_list(all_test, key='at'))
        else:
            await message.answer(text='Пользователь не писал боту')

    # Смена роли пользователя
    elif message.user_shared.request_id == 3:
        if user_in_db:
            roles = db.get_roles()
            await state.update_data(tg_id=message.user_shared.user_id)
            await state.set_state(UpdateRoleUser.update_role)
            await message.answer(text='Выберите роль', reply_markup=keyboard_list(roles, key='cr'))
        else:
            await message.answer(text='Пользователь не писал боту')


async def add_user(message: Message, user_in_db):
    if user_in_db:
        await message.answer(text='Этот пользователь уже есть в базе')
    else:
        try:
            user = await bot.get_chat(message.user_shared.user_id)
        except:
            user = None

        if user:
            username = user.username

            if user.username is None:
                username = f'{user.first_name} {user.last_name if user.last_name else ""}'.strip()

            db.add_user(name=username, tg_id=message.user_shared.user_id)
            await message.answer(text='Пользователь успешно добавлен')
        else:
            await message.answer(text='Пользователь не писал боту')


@router.message(F.text == 'Отчеты', AdminRoleFilter())
async def change_report_tests(message: Message, state: FSMContext):
    all_tests = db.get_all_tests()
    await message.answer(text='Выберите опрос для получения отчета', reply_markup=keyboard_list(all_tests, key='gt'))
    await state.set_state(ReportStates.choosing_test)
