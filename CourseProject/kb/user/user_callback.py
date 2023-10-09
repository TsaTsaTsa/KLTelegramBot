from aiogram import types

import text

end_using_bot_cd = 'end_used_bot_cd'

#
# hello_cd = 'hello_cd'
# hello2_cd = 'hello2_cd'
# about_video_course_text_kb = "Скорее к первому уроку"
# about_video_course_cd = 'about_video_course_cd'
# get_mood_tracker_cd = 'get_mood_tracker_cd'
# get_mood_tracker_text_kb = "Активируем!"
# skip_mood_tracker_text_kb = "Пока нет"
# skip_mood_tracker_cd = 'skip_mood_tracker_cd'
# return_text_kb = "« Назад"
# return_cd = [
#     'return_cd_1',
#     'return_cd_ex_1',
#     'return_cd_2',
#     'return_cd_ex_2',
#     'return_cd_3',
#     'return_cd_ex_3',
#     'return_cd_4',
#     'return_cd_ex_4',
#     'return_cd_5',
#     'return_cd_ex_5',
#     'return_cd_6',
#     'return_cd_end1',
#     'return_cd_end2',
#     'return_cd_end3'
# ]
#
# return_introd_exercises = [
#     'return_in_1_cd',
#     'return_in_2_cd',
#     'return_in_3_cd',
#     'return_in_4_cd',
#     'return_in_5_cd',
# ]
#
# end_course_text = 'Завершить курс »'
# what_else_cd = 'what_else_cd'
# what_else_text_kb = "Что дальше? »"
# to_describe_main_menu_cd = 'to_describe_main_menu_cd'
# to_describe_feeling_track_cd = 'to_describe_feeling_track_cd'
# to_describe_feeling_track_text = 'Очень внимательно читаю. »'
# # select_done_cd = 'select_done_cd'
# # select_undone_cd = 'select_undone_cd'
# to_introduction_cd = ['to_introduction2_cd',
#                       'to_introduction3_cd',
#                       'to_introduction4_cd',
#                       'to_introduction5_cd',
#                       'to_first-exercise_cd']
# end_course_cd = 'end_course_cd'


def user_main_menu_inactive():
    buttons = [
        [types.InlineKeyboardButton(text="Активировать бот", callback_data='activate_bot_cd')],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def deactivate_bot_kb():
    buttons = [
        [types.InlineKeyboardButton(text="Отключить бот...", callback_data='sure_deactivate_bot_cd')],
        [types.InlineKeyboardButton(text="Не отключать", callback_data='dont_deactivate_bot_cd')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
