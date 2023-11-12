import aiogram.types as types


# Клавиатура для Q12
def yes_no_kb(language) -> types.InlineKeyboardMarkup:
    questions = [
        {
            'ru': 'Да',
            'en': 'Yes'
        },
        {
            'ru': 'Нет',
            'en': 'No'
        }
    ]

    buttons = [
        [
            types.InlineKeyboardButton(text=questions[0][language], callback_data="yn_yes"),
            types.InlineKeyboardButton(text=questions[1][language], callback_data="yn_no")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# Клавиатура для eNps
def zero_to_nine() -> types.InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text=f"{num}", callback_data=f"zn_{num}") for num in range(1, 4)],
        [types.InlineKeyboardButton(text=f"{num}", callback_data=f"zn_{num}") for num in range(4, 7)],
        [types.InlineKeyboardButton(text=f"{num}", callback_data=f"zn_{num}") for num in range(7, 10)],
        [types.InlineKeyboardButton(text=f"0", callback_data=f"enps_0")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
