from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton, \
    KeyboardButtonRequestUser


# Клавиатура создается из любого списка
def keyboard_list(items, key: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=f"{item[1]}", callback_data=f"{key}_{item[0]}")] for item in items
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# Клавиатура для пользователя
def keyboard_menu_user(languages_data) -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=languages_data['UserWorks']['Keyboards']['CheckSurveys'])],
        [KeyboardButton(text=languages_data['UserWorks']['Keyboards']['SelectLanguage'])]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# Клавиатура для HR
def keyboard_menu_HR() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(
            text='Назначить опрос сотруднику',
            request_user=KeyboardButtonRequestUser(
                request_id=2,
            )), KeyboardButton(text='Назначить опрос подразделению')],
        [KeyboardButton(
            text='Добавить сотрудника',
            request_user=KeyboardButtonRequestUser(
                request_id=1,
            )
        ), KeyboardButton(
            text='Сменить роль сотруднику',
            request_user=KeyboardButtonRequestUser(
                request_id=3,
            )
        )],
        [KeyboardButton(text='Отчеты')],
        [KeyboardButton(text='Проверить наличие опросов')],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def keyboard_type() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=f"График", callback_data='ct_0')],
        [InlineKeyboardButton(text=f"Общий", callback_data='ct_1')],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
