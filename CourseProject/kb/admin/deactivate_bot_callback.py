from aiogram import types

yes_cd = 'yes_cd'
no_cd = 'no_cd'


def yeas_no_kb():
    buttons = [
        [types.InlineKeyboardButton(text="Да", callback_data=yes_cd),
         types.InlineKeyboardButton(text="Нет", callback_data=no_cd)],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

