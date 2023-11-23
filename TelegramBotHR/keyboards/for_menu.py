from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton, \
    KeyboardButtonRequestUser


# Клавиатура создается из любого списка
def keyboard_list(items, key: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=f"{item[1]}", callback_data=f"{key}_{item[0]}")] for item in items]
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
            text='Назначить опрос пользователю',
            request_user=KeyboardButtonRequestUser(
                request_id=2,
            ))],
        [KeyboardButton(
            text='Добавить пользователя',
            request_user=KeyboardButtonRequestUser(
                request_id=1,
            )
        ), KeyboardButton(
            text='Сменить роль пользователю',
            request_user=KeyboardButtonRequestUser(
                request_id=3,
            )
        )],
        [KeyboardButton(text='Отчеты')],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
