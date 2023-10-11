from enum import Enum

from aiogram import types


class SectionsNames(Enum):
    method_demidov = "Метод Демидова"
    method_knebel = "Метод Кнебель"
    method_chekhov = "Метод Чехова"
    method_stanislavsky = "Метод Станиславского"
    meditation = "Медитации"
    quality = "Качество"
    another = "Другая"


class SectionsCd(Enum):
    method_demidov_cd = "method_demidov_cd"
    method_knebel_cd = "method_knebel_cd"
    method_chekhov_cd = "method_chekhov_cd"
    method_stanislavsky_cd = "method_stanislavsky_cd"
    meditation_cd = "meditation_cd"
    quality_cd = "quality_cd"
    another_cd = "another_cd"


class SectionsId(Enum):
    method_demidov_cd = 1
    method_knebel_cd = 2
    method_chekhov_cd = 3
    method_stanislavsky_cd = 4
    meditation_cd = 5
    quality_cd = 6
    another_cd = 7


return_cd = 'return_cd'
all_exercise_cd = 'all_exercise_cd'


def learning_sections_buttons():
    buttons = [
        [types.InlineKeyboardButton(text=SectionsNames.method_demidov.value,
                                    callback_data=SectionsCd.method_demidov_cd.value)],
        [types.InlineKeyboardButton(text=SectionsNames.method_knebel.value,
                                    callback_data=SectionsCd.method_knebel_cd.value),
         types.InlineKeyboardButton(text=SectionsNames.method_chekhov.value,
                                    callback_data=SectionsCd.method_chekhov_cd.value)],
        [types.InlineKeyboardButton(text=SectionsNames.method_stanislavsky.value,
                                    callback_data=SectionsCd.method_stanislavsky_cd.value)],
        [types.InlineKeyboardButton(text=SectionsNames.meditation.value, callback_data=SectionsCd.meditation_cd.value),
         types.InlineKeyboardButton(text=SectionsNames.quality.value, callback_data=SectionsCd.quality_cd.value)],
        [types.InlineKeyboardButton(text=SectionsNames.another.value, callback_data=SectionsCd.another_cd.value)],
        [types.InlineKeyboardButton(text="« Назад", callback_data=return_cd)]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def learning_sections_exercise_buttons():
    buttons = [[types.InlineKeyboardButton(text=SectionsNames.method_demidov.value,
                                           callback_data=SectionsCd.method_demidov_cd.value)],
               [types.InlineKeyboardButton(text=SectionsNames.method_knebel.value,
                                           callback_data=SectionsCd.method_knebel_cd.value),
                types.InlineKeyboardButton(text=SectionsNames.method_chekhov.value,
                                           callback_data=SectionsCd.method_chekhov_cd.value)],
               [types.InlineKeyboardButton(text=SectionsNames.method_stanislavsky.value,
                                           callback_data=SectionsCd.method_stanislavsky_cd.value)],
               [types.InlineKeyboardButton(text=SectionsNames.meditation.value,
                                           callback_data=SectionsCd.meditation_cd.value),
                types.InlineKeyboardButton(text=SectionsNames.quality.value,
                                           callback_data=SectionsCd.quality_cd.value)],
               [types.InlineKeyboardButton(text=SectionsNames.another.value,
                                           callback_data=SectionsCd.another_cd.value)],
               [types.InlineKeyboardButton(text="Все упражнения", callback_data=all_exercise_cd)],
    [types.InlineKeyboardButton(text="« Назад", callback_data=return_cd)]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
