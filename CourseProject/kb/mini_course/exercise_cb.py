from aiogram import types

return_text_kb = "« Назад"
return_exercise_cd = "return_exercise_cd"
to_lesson_cd = 'to_lesson_cd'
close_mini_course_cd = "close_mini_course_cd"

to_lesson_text_kb = ['Ко 2-ому уроку »',
                   'К 3-ему уроку »',
                   'К 4-ому уроку »',
                   'К 5-ому уроку »',
                   'К 6-ому уроку »',
                   'Завершить курс »']


def generate_exercise_kb(id_ex: int):
    buttons = [
        [
            types.InlineKeyboardButton(text=return_text_kb, callback_data=return_exercise_cd),
            types.InlineKeyboardButton(text=to_lesson_text_kb[id_ex], callback_data=to_lesson_cd),
        ],
        [types.InlineKeyboardButton(text="Закрыть", callback_data=close_mini_course_cd)]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def generate_exercise_user_first_time_kb(id_ex: int):
    buttons = [
        [
            types.InlineKeyboardButton(text=return_text_kb, callback_data=return_exercise_cd),
            types.InlineKeyboardButton(text=to_lesson_text_kb[id_ex], callback_data=to_lesson_cd),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def get_exercise_kb(is_first_time: bool, id_intro: int):
    if is_first_time:
        return generate_exercise_user_first_time_kb(id_intro)
    return generate_exercise_kb(id_intro)
