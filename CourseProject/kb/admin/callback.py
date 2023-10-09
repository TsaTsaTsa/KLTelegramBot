from aiogram import types

add_text_cd = "add_text"
add_text_text_kb = "Добавить текст"
skip_text_text_kb = "Без текста"
skip_text_cd = "skip_text"
return_text_kb = "« Назад"
return_cd = "return_to"
add_photo_text_kb = "Добавить фото"
add_photo_text_cd = "add_photo"
end_create_post_text_cd = "end_create_post"
end_create_post_text_kb = "Завершить"
continue_without_text_text_kb = "Удалить текст"
continue_without_text_text_cd = "continue_without_text"
continue_without_photo_cd = "continue_without_photo"
continue_without_photo_text_kb = "Удалить фото"
do_something_with_post_cd = "do_something_with_post"
do_something_with_post_kb = "Да"
choose_another_post_cd = "choose_another"
choose_another_post_kb = "Ввести другой id"
end_update_text_kb = "Готово"
end_update_text_cd = "end_update"
choose_photo_to_update_text_kb = "Фото"
choose_photo_to_update_text_cd = "choose_photo_to_update"
choose_text_to_update_text_cd = "choose_text_to_update"
choose_text_to_update_text_kb = "Текст"
return_to_item_menu_cd = 'return_to_item_menu'
return_to_item_menu_kb = 'Нет'


# inactive_main_menu_buttons = [
#     [types.InlineKeyboardButton(text=create_post_text_kb, callback_data=create_post_cd)],
#     [types.InlineKeyboardButton(text=create_exercise_text_kb, callback_data=create_exercise_cd)],
#     [types.InlineKeyboardButton(text=update_text_kb, callback_data=update_cd),
#      types.InlineKeyboardButton(text=delete_post_main_text_kb, callback_data=delete_post_cd)],
#     [types.InlineKeyboardButton(text=mini_course_text_kb, callback_data=mini_course_cd),
#      types.InlineKeyboardButton(text="Статистика", callback_data='statistics_cd')],
#     [types.InlineKeyboardButton(text="Несделанные упражнения", callback_data='dont_exercises_cd')],
#     [types.InlineKeyboardButton(text="Все упражнения", callback_data='all_exercises_cd')],
#     [types.InlineKeyboardButton(text="Включить трекер чувств", callback_data=activate_feeling_tracker_cd)],
#     [types.InlineKeyboardButton(text="Отключить бот", callback_data='deactivate_boss_cd')]
# ]
#
# active_main_menu_buttons = [
#     [types.InlineKeyboardButton(text=create_post_text_kb, callback_data=create_post_cd)],
#     [types.InlineKeyboardButton(text=create_exercise_text_kb, callback_data=create_exercise_cd)],
#     [types.InlineKeyboardButton(text=update_text_kb, callback_data=update_cd),
#      types.InlineKeyboardButton(text=delete_post_main_text_kb, callback_data=delete_post_cd)],
#     [types.InlineKeyboardButton(text=mini_course_text_kb, callback_data=mini_course_cd),
#      types.InlineKeyboardButton(text="Статистика", callback_data='statistics_cd')],
#     [types.InlineKeyboardButton(text="Несделанные упражнения", callback_data='dont_exercises_cd')],
#     [types.InlineKeyboardButton(text="Все упражнения", callback_data='all_exercises_cd')],
#     [types.InlineKeyboardButton(text="Выключить трекер чувств", callback_data=inactivate_feeling_tracker_cd)],
#     [types.InlineKeyboardButton(text="Отключить бот", callback_data='deactivate_boss_cd')]
# ]
#
#
# def get_admin_main_menu_kb(is_active: bool):
#     if is_active:
#         return types.InlineKeyboardMarkup(inline_keyboard=active_main_menu_buttons)
#     return types.InlineKeyboardMarkup(inline_keyboard=inactive_main_menu_buttons)


def return_kb():
    buttons = [
        [types.InlineKeyboardButton(text=return_text_kb, callback_data=return_cd)]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_admin_new_post_menu_kb():
    buttons = [
        [
            types.InlineKeyboardButton(text=add_text_text_kb, callback_data=add_text_cd),
            types.InlineKeyboardButton(text=skip_text_text_kb, callback_data=skip_text_cd)
        ],
        [types.InlineKeyboardButton(text=return_text_kb, callback_data=return_cd)]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_admin_add_photo_menu_kb():
    buttons = [
        [
            types.InlineKeyboardButton(text=add_photo_text_kb, callback_data=add_photo_text_cd),
            types.InlineKeyboardButton(text=end_create_post_text_kb, callback_data=end_create_post_text_cd)
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_update_photo_menu_kb():
    buttons = [
        [
            types.InlineKeyboardButton(text=add_photo_text_kb, callback_data=add_photo_text_cd),
            types.InlineKeyboardButton(text=continue_without_photo_text_kb, callback_data=continue_without_photo_cd)
        ],
        [types.InlineKeyboardButton(text=return_text_kb, callback_data=return_cd)]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def choose_post_id_kb():
    buttons = [
        [types.InlineKeyboardButton(text=do_something_with_post_kb, callback_data=do_something_with_post_cd),
         types.InlineKeyboardButton(text=choose_another_post_kb, callback_data=choose_another_post_cd)],
        [types.InlineKeyboardButton(text=return_text_kb, callback_data=return_cd)]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def choose_item_to_update_kb():
    buttons = [
        [types.InlineKeyboardButton(text=choose_text_to_update_text_kb, callback_data=choose_text_to_update_text_cd),
         types.InlineKeyboardButton(text=choose_photo_to_update_text_kb, callback_data=choose_photo_to_update_text_cd)],
        [types.InlineKeyboardButton(text=end_update_text_kb, callback_data=end_update_text_cd)]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def continue_with_out_text_kb():
    buttons = [
        [types.InlineKeyboardButton(text=return_text_kb, callback_data=return_cd),
         types.InlineKeyboardButton(text=continue_without_text_text_kb, callback_data=continue_without_text_text_cd)],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def delete_or_update_post_kb():
    buttons = [
        [types.InlineKeyboardButton(text=do_something_with_post_kb, callback_data=do_something_with_post_cd),
         types.InlineKeyboardButton(text=return_to_item_menu_kb, callback_data=return_to_item_menu_cd)],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard



yes_cd = 'yes_cd'
no_cd = 'no_cd'


def on_off_feeling_tracker_kb():
    buttons = [
        [
            types.InlineKeyboardButton(text="Да", callback_data=yes_cd),
            types.InlineKeyboardButton(text="Нет", callback_data=no_cd),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
