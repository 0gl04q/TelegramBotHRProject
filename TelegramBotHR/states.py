from aiogram.fsm.state import StatesGroup, State

'''
    Файл для установки стадий разных конечных автоматов
'''


class MenuStates(StatesGroup):
    choosing_test = State()
    choosing_action = State()
    choosing_language = State()


class TestStates(StatesGroup):
    passing_test = State()


class AddUser(StatesGroup):
    change_department = State()
    add_user = State()


class AddTestUser(StatesGroup):
    choosing_test = State()


class AddTestDepartment(StatesGroup):
    choosing_department = State()
    choosing_test = State()


class UpdateRoleUser(StatesGroup):
    update_role = State()


class ReportStates(StatesGroup):
    choosing_type = State()
    choosing_test = State()
