from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton, \
    KeyboardButtonRequestUser


# Клавиатура создается из любого списка
def keyboard_list(items, key: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=f"{item[1]}", callback_data=f"{key}_{item[0]}")] for item in items]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# Клавиатура для пользователя
def keyboard_menu_user(language='ru') -> ReplyKeyboardMarkup:
    questions = [
        {
            'ru': 'Проверить наличие опросов',
            'en': 'View survey availability'
        },
        {
            'ru': 'Выбрать язык',
            'en': 'Select language'
        }
    ]

    keyboard = [
        [KeyboardButton(text=questions[0][language])],
        [KeyboardButton(text=questions[1][language])]
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
