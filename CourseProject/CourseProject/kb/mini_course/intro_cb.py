from aiogram import types

introduce_kb_texts = ['Так-так »', 'Угу. »', '»»', 'Идем дальше »', "К упражнению »"]
return_text_kb = "« Назад"
return_intro_cd = "return_intro_cd"
to_exercise_text_kb = 'К упражнению »'
to_intro_cd = 'to_intro_cd'
close_mini_course_cd = "close_mini_course_cd"


def generate_intro_kb(id_intro: int):
    buttons = [
        [
            types.InlineKeyboardButton(text=return_text_kb, callback_data=return_intro_cd),
            types.InlineKeyboardButton(text=introduce_kb_texts[id_intro], callback_data=to_intro_cd),
        ],
        [types.InlineKeyboardButton(text="Закрыть", callback_data=close_mini_course_cd)]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def generate_intro_user_first_time_kb(id_ex: int):
    buttons = [
        [
            types.InlineKeyboardButton(text=return_text_kb, callback_data=return_intro_cd),
            types.InlineKeyboardButton(text=introduce_kb_texts[id_ex], callback_data=to_intro_cd),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def get_intro_kb(is_first_time: bool, id_intro: int):
    if is_first_time:
        return generate_intro_user_first_time_kb(id_intro)
    return generate_intro_kb(id_intro)
