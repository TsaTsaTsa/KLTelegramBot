from aiogram import types
from aiogram.filters import state
from sqlalchemy import select

from database.database import get_async_session
from models.users import Status

main_menu_button_text = ["Добавить пост",
                         "Добавить упражнение",
                         "Редактировать пост",
                         "Удалить пост",
                         "Мини курс",
                         "Статистика",
                         "Несделанные упражнения",
                         "Все упражнения",
                         "Отключить бот"]
to_on_feeling_tracker_text = "Включить Трекер Чувств"
to_off_feeling_tracker_text = "Выключить Трекер Чувств"

create_post_cd = "create_post_cd"
create_exercise_cd = "create_exercise_cd"
update_cd = "update_post"
delete_post_cd = "delete_post_cd"
mini_course_cd = "mini_course_cd"
statistics_cd = "statistics_cd"
do_not_exercises_cd = "do_not_exercises_cd"
all_exercises_cd = "all_exercises_cd"
to_on_feeling_tracker_cd = "to_on_feeling_tracker_cd"
to_off_feeling_tracker_cd = "to_off_feeling_tracker_cd"
deactivate_bot_cd = "deactivate_bot_cd"
activate_bot_cd = 'activate_bot_cd'


off_track_main_menu_buttons = [
    [types.InlineKeyboardButton(text=main_menu_button_text[0], callback_data=create_post_cd)],
    [types.InlineKeyboardButton(text=main_menu_button_text[1], callback_data=create_exercise_cd)],
    [types.InlineKeyboardButton(text=main_menu_button_text[2], callback_data=update_cd),
     types.InlineKeyboardButton(text=main_menu_button_text[3], callback_data=delete_post_cd)],
    [types.InlineKeyboardButton(text=main_menu_button_text[4], callback_data=mini_course_cd),
     types.InlineKeyboardButton(text=main_menu_button_text[5], callback_data=statistics_cd)],
    [types.InlineKeyboardButton(text=main_menu_button_text[6], callback_data=do_not_exercises_cd)],
    [types.InlineKeyboardButton(text=main_menu_button_text[7], callback_data=all_exercises_cd)],
    [types.InlineKeyboardButton(text=to_on_feeling_tracker_text, callback_data=to_on_feeling_tracker_cd)],
    [types.InlineKeyboardButton(text=main_menu_button_text[8], callback_data=deactivate_bot_cd)]
]


on_track_main_menu_buttons = [
    [types.InlineKeyboardButton(text=main_menu_button_text[0], callback_data=create_post_cd)],
    [types.InlineKeyboardButton(text=main_menu_button_text[1], callback_data=create_exercise_cd)],
    [types.InlineKeyboardButton(text=main_menu_button_text[2], callback_data=update_cd),
     types.InlineKeyboardButton(text=main_menu_button_text[3], callback_data=delete_post_cd)],
    [types.InlineKeyboardButton(text=main_menu_button_text[4], callback_data=mini_course_cd),
     types.InlineKeyboardButton(text=main_menu_button_text[5], callback_data=statistics_cd)],
    [types.InlineKeyboardButton(text=main_menu_button_text[6], callback_data=do_not_exercises_cd)],
    [types.InlineKeyboardButton(text=main_menu_button_text[7], callback_data=all_exercises_cd)],
    [types.InlineKeyboardButton(text=to_off_feeling_tracker_text, callback_data=to_off_feeling_tracker_cd)],
    [types.InlineKeyboardButton(text=main_menu_button_text[8], callback_data=deactivate_bot_cd)]
]


deactivate_bot_main_menu_buttons = [
    [types.InlineKeyboardButton(text=main_menu_button_text[0], callback_data=create_post_cd)],
    [types.InlineKeyboardButton(text=main_menu_button_text[1], callback_data=create_exercise_cd)],
    [types.InlineKeyboardButton(text=main_menu_button_text[2], callback_data=update_cd),
     types.InlineKeyboardButton(text=main_menu_button_text[3], callback_data=delete_post_cd)],
    [types.InlineKeyboardButton(text="Активировать бот", callback_data=activate_bot_cd)]
]


def get_deactivate_admin_main_menu_kb():
    return types.InlineKeyboardMarkup(inline_keyboard=deactivate_bot_main_menu_buttons)


def get_admin_main_menu_kb(status: Status):
    if status == Status.on_feeling_tracker.value:
        return types.InlineKeyboardMarkup(inline_keyboard=on_track_main_menu_buttons)
    if status == Status.off_feeling_tracker.value:
        return types.InlineKeyboardMarkup(inline_keyboard=off_track_main_menu_buttons)
    if status == Status.inactive.value:
        return types.InlineKeyboardMarkup(inline_keyboard=deactivate_bot_main_menu_buttons)
