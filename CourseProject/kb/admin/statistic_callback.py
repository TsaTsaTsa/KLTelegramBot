from aiogram import types


close_cd = 'close_cd'

def close_statistic_kb():
    buttons = [
        [types.InlineKeyboardButton(text="Закрыть", callback_data=close_cd)]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
