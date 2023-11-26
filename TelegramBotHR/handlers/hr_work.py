from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import db
from func.menu_func import start_check
from keyboards.for_menu import keyboard_list, keyboard_menu_user, keyboard_type
from filters import AdminRoleFilter
from states import AddTestUser, MenuStates, UpdateRoleUser, ReportStates, AddUser, AddTestDepartment
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value
)
from main import bot
import languages.languages as lg
from graphics.graph import create_graph
from aiogram.types import InputFile
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
router = Router()


@router.callback_query(AddTestUser.choosing_test, F.data.startswith("at_"))
async def add_test_user(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    tg_id = user_data['tg_id']
    test_id = callback.data.split("_")[1]

    if db.check_test_result_user(tg_id, test_id):
        await callback.message.edit_text(text='Этот опрос уже добавлен сотруднику')
    else:
        db.add_test_result_user(tg_id, test_id)
        await callback.message.edit_text(text='Опрос успешно добавлен сотруднику')
    await state.set_state(MenuStates.choosing_action)


@router.callback_query(UpdateRoleUser.update_role, F.data.startswith("cr_"))
async def update_role_user(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    tg_id = user_data['tg_id']
    role_id = callback.data.split("_")[1]

    db.update_role_user(tg_id, role_id)
    await callback.message.edit_text(text='Роль сотруднику установлена')
    await state.set_state(MenuStates.choosing_action)


@router.callback_query(ReportStates.choosing_test, F.data.startswith("gt_"))
async def get_report_test(callback: CallbackQuery, state: FSMContext):
    test_id = callback.data.split("_")[1]
    state_data = await state.get_data()
    type_id = state_data['type_id']

    if type_id:
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
    else:
        data = dict(db.get_result_graph(test_id))

        name_file = await create_graph(data)

        image_from_pc = FSInputFile(name_file)
        await callback.message.answer_photo(
            image_from_pc,
            caption='График'
        )

@router.message(F.user_shared, AdminRoleFilter())
async def get_shared_user(message: Message, state: FSMContext):
    user_in_db = db.get_user_by_id(tg_id=message.user_shared.user_id)

    # Дефолтный язык русский
    language_data = lg.get_languages_data()['ru']

    # Добавление пользователя
    if message.user_shared.request_id == 1:
        if not user_in_db:
            await state.set_state(AddUser.add_user)
            await state.update_data(
                user_in_db=user_in_db,
                language_data=language_data,
                shared_user=message.user_shared.user_id
            )

            departments = db.get_departments()
            await message.answer(
                text='Выберите подразделение',
                reply_markup=keyboard_list(departments, key='dep')
            )

        else:
            await message.answer(text='Сотрудник уже добавлен в бота')

    # Назначение теста пользователю
    elif message.user_shared.request_id == 2:
        if user_in_db:
            all_test = db.get_all_tests()
            await state.update_data(tg_id=message.user_shared.user_id)
            await state.set_state(AddTestUser.choosing_test)
            await message.answer(
                text='Выберите опрос',
                reply_markup=keyboard_list(all_test, key='at')
            )

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


@router.callback_query(AddUser.add_user, F.data.startswith('dep_'))
async def add_user(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    user_in_db = state_data['user_in_db']
    language_data = state_data['language_data']
    shared_user = state_data['shared_user']
    department_id = callback.data.split("_")[1]

    if user_in_db:
        await callback.message.edit_text(text='Этот сотрудник уже есть в базе')
    else:
        try:
            user = await bot.get_chat(shared_user)
        except:
            user = None

        if user:
            username = user.username

            if user.username is None:
                username = f'{user.first_name} {user.last_name if user.last_name else ""}'.strip()

            db.add_user(
                name=username,
                tg_id=shared_user,
                department_id=department_id,
                role_id=0 if department_id == '0' else 1
            )

            await callback.message.edit_text(text='Сотрудник успешно добавлен')

            await state.set_state(MenuStates.choosing_action)
            await bot.send_message(
                chat_id=shared_user,
                text='Вас добавили в HR бота!',
                reply_markup=keyboard_menu_user(language_data)
            )
        else:
            await callback.message.edit_text(text='Пользователь не писал боту')


@router.message(F.text == 'Отчеты', AdminRoleFilter())
async def change_report_type(message: Message, state: FSMContext):
    await message.answer(
        text='Выберите вид отчета',
        reply_markup=keyboard_type()
    )
    await state.set_state(ReportStates.choosing_type)


@router.callback_query(ReportStates.choosing_type)
async def change_report_test(callback: CallbackQuery, state: FSMContext):
    type_id = int(callback.data.split("_")[1])
    all_tests = db.get_all_tests()
    await callback.message.edit_text(text='Выберите опрос для получения отчета',
                                     reply_markup=keyboard_list(all_tests, key='gt'))
    await state.set_state(ReportStates.choosing_test)
    await state.update_data(type_id=type_id)


@router.message(F.text == 'Назначить опрос подразделению', AdminRoleFilter())
async def change_department(message: Message, state: FSMContext):
    departments = db.get_departments()
    await state.set_state(AddTestDepartment.choosing_department)
    await message.answer(
        text='Выберите подразделение',
        reply_markup=keyboard_list(departments, key='dep')
    )


@router.message(F.text == 'Проверить наличие опросов', AdminRoleFilter())
async def change_survey(message: Message, state: FSMContext):
    await start_check(message.answer, message.from_user, state)


@router.callback_query(AddTestDepartment.choosing_department, F.data.startswith('dep_'))
async def change_department_test(callback: CallbackQuery, state: FSMContext):
    all_tests = db.get_all_tests()
    department_id = callback.data.split("_")[1]
    await state.set_state(AddTestDepartment.choosing_test)
    await state.update_data(department_id=department_id)
    await callback.message.edit_text(
        text='Выберите опрос',
        reply_markup=keyboard_list(all_tests, key='at')
    )


@router.callback_query(AddTestDepartment.choosing_test, F.data.startswith('at_'))
async def add_department_test(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    department_id = state_data['department_id']
    test_id = callback.data.split("_")[1]

    users = db.get_users_by_department(department_id)

    for user in users:
        if not db.check_test_result_user(user[0], test_id):
            db.add_test_result_user(user[0], test_id)

    await callback.message.edit_text(
        text='Опросы успешно назначены'
    )
