from aiogram import types


texts_ref_to_lessons = ['Первый урок', 'Второй урок', 'Третий урок', 'Четвертый урок', 'Пятый урок', 'Шестой урок']
ref_to_lessons = [
    'https://youtu.be/jj7Rf7mp4zE?si=-7SubK2AvbGBpjwx',
    'https://youtu.be/FmxH_c_TNss?si=3ft8AIDubWdYrD5m',
    'https://youtu.be/fz1fY_MSN6o?si=-dVF-GwtFTwEE6iN',
    'https://youtu.be/F7tLHsRVWvw?si=8v8fKxERt95vqq3A',
    'https://youtu.be/sGYsS2cvVYo?si=xYODOKSV5NEB6iKz',
    'https://youtu.be/a4Vpj8-eBrY?si=dmtMK5KChRHDmn2l'
]
return_text_kb = "« Назад"
return_lesson_cd = "return_lesson_cd"
to_exercise_text_kb = 'К упражнению »'
to_exercise_cd = 'to_exercise_cd'
close_mini_course_cd = "close_mini_course_cd"
end_course_cd = 'end_course_cd'

def generate_lesson_time_kb(les_id: int):
    buttons = [
        [types.InlineKeyboardButton(text=texts_ref_to_lessons[les_id], url=ref_to_lessons[les_id])],
        [
            types.InlineKeyboardButton(text=return_text_kb, callback_data=return_lesson_cd),
            types.InlineKeyboardButton(text=to_exercise_text_kb, callback_data=to_exercise_cd),
        ],
        [types.InlineKeyboardButton(text="Закрыть", callback_data=close_mini_course_cd)]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def generate_lesson_user_first_time_kb(id_cl: int):
    buttons = [
        [types.InlineKeyboardButton(text=texts_ref_to_lessons[id_cl], url=ref_to_lessons[id_cl])],
        [
            types.InlineKeyboardButton(text=return_text_kb, callback_data=return_lesson_cd),
            types.InlineKeyboardButton(text=to_exercise_text_kb, callback_data=to_exercise_cd),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def get_kb(is_first_time: bool, les_id: int):
    if is_first_time:
        return generate_lesson_user_first_time_kb(les_id)
    return generate_lesson_time_kb(les_id)


def first_lessen_kb():
    buttons = [
        [types.InlineKeyboardButton(text=texts_ref_to_lessons[0], url=ref_to_lessons[0])],
        [types.InlineKeyboardButton(text=to_exercise_text_kb, callback_data=to_exercise_cd)],
        [types.InlineKeyboardButton(text="Закрыть", callback_data=close_mini_course_cd)]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def first_lessen_user_first_time_kb():
    buttons = [
        [types.InlineKeyboardButton(text=texts_ref_to_lessons[0], url=ref_to_lessons[0])],
        [types.InlineKeyboardButton(text=to_exercise_text_kb, callback_data=to_exercise_cd)],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def get_first_les_kb(is_first_time: bool):
    if is_first_time:
        return first_lessen_user_first_time_kb()
    return first_lessen_kb()


def end_course_kb():
    buttons = [
        [
            types.InlineKeyboardButton(text=return_text_kb, callback_data=return_lesson_cd),
            types.InlineKeyboardButton(text="❤️", callback_data=end_course_cd),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
