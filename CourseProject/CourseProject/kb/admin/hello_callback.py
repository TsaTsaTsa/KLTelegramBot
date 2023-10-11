from aiogram import types

help_cd = 'help_cd'
next_cd = 'next_cd'


def help_kb():
    buttons = [
        [types.InlineKeyboardButton(text="Привет!", callback_data=help_cd)]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def next_kb():
    buttons = [
        [types.InlineKeyboardButton(text="»»", callback_data=next_cd)]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
