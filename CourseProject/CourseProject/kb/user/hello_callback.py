from aiogram import types

hello_cd = 'hello_cd'
main_info_cd = 'main_info_cd'


def hello1_kb():
    buttons = [
        [types.InlineKeyboardButton(text="Привет! »", callback_data=hello_cd)],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def hello2_kb():
    buttons = [
        [types.InlineKeyboardButton(text="Красота! »", callback_data=hello_cd)],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def hello3_kb():
    buttons = [
        [types.InlineKeyboardButton(text="К 1-ому уроку »", callback_data=hello_cd)],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def main_info1():
    buttons = [
        [types.InlineKeyboardButton(text="Внимательно читаю »", callback_data=main_info_cd)]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def main_info2():
    buttons = [
        [types.InlineKeyboardButton(text='Ага. »', callback_data=main_info_cd)],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
