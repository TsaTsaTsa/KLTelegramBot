from aiogram import types


def return_kb():
    buttons = [
        [types.InlineKeyboardButton(text="« Назад", callback_data='return_cd')],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def end_kb():
    buttons = [
        [types.InlineKeyboardButton(text="Завершить", callback_data='end_cd')],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_felling_describe():
    buttons = [
        [types.InlineKeyboardButton(text="Дополнить чувство", callback_data='sup_describe_cd')],
        [types.InlineKeyboardButton(text="Чувствую, что не хочу...", callback_data='skip_describe_cd')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


emotion_joy_cd = 'emotion_joy_cd'
emotion_calm_cd = 'emotion_calm_cd'
emotion_fatigue_cd ='emotion_fatigue_cd'
emotion_anxiety_cd = 'emotion_anxiety_cd'
emotion_angry_cd = 'emotion_angry_cd'
emotion_user_text_cd = 'emotion_user_text_cd'


def mood_tracker_main_menu():
    buttons = [
        [types.InlineKeyboardButton(text="Радость", callback_data=emotion_joy_cd),
         types.InlineKeyboardButton(text="Спокойствие", callback_data=emotion_calm_cd)],
        [types.InlineKeyboardButton(text="Усталость", callback_data=emotion_fatigue_cd),
         types.InlineKeyboardButton(text="Тревожность", callback_data=emotion_anxiety_cd)],
        [types.InlineKeyboardButton(text="Злость", callback_data=emotion_angry_cd),
         types.InlineKeyboardButton(text="Напишу сам", callback_data=emotion_user_text_cd)],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
