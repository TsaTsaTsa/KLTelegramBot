from aiogram import types

select_done_cd = 'select_done_cd'
select_undone_cd = 'select_undone_cd'
exercise_forward_cd = 'exercise_forward_cd'
exercise_close_cd = 'exercise_close_cd'
exercise_back_cd = 'exercise_back_cd'


def exercise_forward_done_kb():
    buttons = [
        [types.InlineKeyboardButton(text="Отметить как невыполненное", callback_data=select_undone_cd)],
        [types.InlineKeyboardButton(text="»", callback_data=exercise_forward_cd)],
        [types.InlineKeyboardButton(text="Закрыть", callback_data=exercise_close_cd)],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def exercise_forward_undone_kb():
    buttons = [
        [types.InlineKeyboardButton(text="Отметить как выполненное", callback_data=select_done_cd)],
        [types.InlineKeyboardButton(text="»", callback_data=exercise_forward_cd)],
        [types.InlineKeyboardButton(text="Закрыть", callback_data=exercise_close_cd)],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def exercise_back_done_kb():
    buttons = [
        [types.InlineKeyboardButton(text="Отметить как невыполненное", callback_data=select_undone_cd)],
        [types.InlineKeyboardButton(text="«", callback_data=exercise_back_cd)],
        [types.InlineKeyboardButton(text="Закрыть", callback_data=exercise_close_cd)],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def exercise_back_undone_kb():
    buttons = [
        [types.InlineKeyboardButton(text="Отметить как выполненное", callback_data=select_done_cd)],
        [types.InlineKeyboardButton(text="«", callback_data=exercise_back_cd)],
        [types.InlineKeyboardButton(text="Закрыть", callback_data=exercise_close_cd)],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def exercise_forward_back_done_kb():
    buttons = [
        [types.InlineKeyboardButton(text="Отметить как невыполненное", callback_data=select_undone_cd)],
        [types.InlineKeyboardButton(text="«", callback_data=exercise_back_cd),
         types.InlineKeyboardButton(text="»", callback_data=exercise_forward_cd)],
        [types.InlineKeyboardButton(text="Закрыть", callback_data=exercise_close_cd)],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def exercise_forward_back_undone_kb():
    buttons = [
        [types.InlineKeyboardButton(text="Отметить как выполненное", callback_data=select_done_cd)],
        [types.InlineKeyboardButton(text="«", callback_data=exercise_back_cd),
         types.InlineKeyboardButton(text="»", callback_data=exercise_forward_cd)],
        [types.InlineKeyboardButton(text="Закрыть", callback_data=exercise_close_cd)]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def exercise_undone_kb():
    buttons = [
        [types.InlineKeyboardButton(text="Отметить как выполненное", callback_data=select_done_cd)],
        [types.InlineKeyboardButton(text="Закрыть", callback_data=exercise_close_cd)]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def exercise_done_kb():
    buttons = [
        [types.InlineKeyboardButton(text="Отметить как невыполненное", callback_data=select_undone_cd)],
        [types.InlineKeyboardButton(text="Закрыть", callback_data=exercise_close_cd)]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
