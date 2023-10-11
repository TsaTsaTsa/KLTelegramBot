from aiogram import types


about_traker_cd = 'about_traker_cd'
get_tracker_cd = 'get_tracker_cd'
skip_tracker_cd = 'skip_tracker_cd'


def about_traker_kb():
    buttons = [
        [types.InlineKeyboardButton(text='»»', callback_data=about_traker_cd)],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_skip_tracker_kb():
    buttons = [
        [types.InlineKeyboardButton(text="Активируем!", callback_data=get_tracker_cd)],
        [types.InlineKeyboardButton(text="Пока нет(", callback_data=skip_tracker_cd)],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def end_help_kb():
    buttons = [
        [types.InlineKeyboardButton(text='❤️', callback_data=about_traker_cd)],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
