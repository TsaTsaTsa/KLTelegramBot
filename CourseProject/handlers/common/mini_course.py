from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from core.config import ADMIN
from handlers import help_functions
from handlers.common import print_menu
from handlers.users import hello
from kb import admin
from kb.mini_course import lesson_cb, intro_cb, exercise_cb
from kb.user import hello_callback
from kb.user.main_menu_callback import mini_course_cd
from models.users import Status
from res.media_files.media_files_id import url_video_class, url_intro_exercise
from res.texts.mini_course import intro_texts, exercise_texts
from states.admin_states import AdminState
from states.mini_course_states import Lesson, IntroExercise, Exercise
from states.user_states import UserHello, UserState

router_mini_course = Router()


@router_mini_course.callback_query(F.data == mini_course_cd, UserState.user_default)
@router_mini_course.callback_query(F.data == intro_cb.return_intro_cd, IntroExercise.intro1)
@router_mini_course.callback_query(F.data == hello_callback.hello_cd, UserHello.hello3)
@router_mini_course.callback_query(F.data == admin.main_menu.mini_course_cd, AdminState.admin_default)
async def first_class_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Lesson.first_lesson)
    await callback.message.delete()
    await callback.message.answer_photo(photo=url_video_class[0],
                                        reply_markup=await lesson_cb.get_first_les_kb(await help_functions.get_status(
                                            callback.message.chat.id) == Status.coursing.value))
    await callback.answer()


@router_mini_course.callback_query(F.data == intro_cb.return_intro_cd, IntroExercise.intro2)
@router_mini_course.callback_query(F.data == lesson_cb.to_exercise_cd, Lesson.first_lesson)
async def intro_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(IntroExercise.intro1)

    await callback.message.delete()
    await callback.message.answer_photo(photo=url_intro_exercise[0],
                                        caption=intro_texts.intro_text1,
                                        reply_markup=await intro_cb.get_intro_kb(await help_functions.get_status(
                                            callback.message.chat.id) == Status.coursing.value, 0),
                                        disable_web_page_preview=True)
    await callback.answer()


@router_mini_course.callback_query(F.data == intro_cb.return_intro_cd, IntroExercise.intro3)
@router_mini_course.callback_query(F.data == intro_cb.to_intro_cd, IntroExercise.intro1)
async def intro_2(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(IntroExercise.intro2)

    await callback.message.delete()
    await callback.message.answer_photo(photo=url_intro_exercise[1],
                                        caption=intro_texts.intro_text2,
                                        reply_markup=await intro_cb.get_intro_kb(await help_functions.get_status(
                                            callback.message.chat.id) == Status.coursing.value, 1),
                                        disable_web_page_preview=True)
    await callback.answer()


@router_mini_course.callback_query(F.data == intro_cb.return_intro_cd, IntroExercise.intro4)
@router_mini_course.callback_query(F.data == intro_cb.to_intro_cd, IntroExercise.intro2)
async def intro_3(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(IntroExercise.intro3)

    await callback.message.delete()
    await callback.message.answer_photo(photo=url_intro_exercise[2],
                                        caption=intro_texts.intro_text3,
                                        reply_markup=await intro_cb.get_intro_kb(await help_functions.get_status(
                                            callback.message.chat.id) == Status.coursing.value, 2),
                                        disable_web_page_preview=True)
    await callback.answer()


@router_mini_course.callback_query(F.data == intro_cb.return_intro_cd, IntroExercise.intro5)
@router_mini_course.callback_query(F.data == intro_cb.to_intro_cd, IntroExercise.intro3)
async def intro_4(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(IntroExercise.intro4)

    await callback.message.delete()
    await callback.message.answer_photo(photo=url_intro_exercise[3],
                                        caption=intro_texts.intro_text4,
                                        reply_markup=await intro_cb.get_intro_kb(await help_functions.get_status(
                                            callback.message.chat.id) == Status.coursing.value, 3),
                                        disable_web_page_preview=True)
    await callback.answer()


@router_mini_course.callback_query(F.data == exercise_cb.return_exercise_cd, Exercise.first_exercise)
@router_mini_course.callback_query(F.data == intro_cb.to_intro_cd, IntroExercise.intro4)
async def intro_5(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(IntroExercise.intro5)

    await callback.message.delete()
    await callback.message.answer_photo(photo=url_intro_exercise[4],
                                        caption=intro_texts.intro_text5,
                                        reply_markup=await intro_cb.get_intro_kb(await help_functions.get_status(
                                            callback.message.chat.id) == Status.coursing.value, 4),
                                        disable_web_page_preview=True)
    await callback.answer()


@router_mini_course.callback_query(F.data == lesson_cb.return_lesson_cd, Lesson.second_lesson)
@router_mini_course.callback_query(F.data == intro_cb.to_intro_cd, IntroExercise.intro5)
async def first_exercise_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Exercise.first_exercise)

    await callback.message.delete()
    await callback.message.answer(text=exercise_texts.ex_texts[0],
                                  reply_markup=await exercise_cb.get_exercise_kb(await help_functions.get_status(
                                            callback.message.chat.id) == Status.coursing.value, 0),
                                  disable_web_page_preview=True)
    await callback.answer()


@router_mini_course.callback_query(F.data == exercise_cb.return_exercise_cd, Exercise.second_exercise)
@router_mini_course.callback_query(F.data == exercise_cb.to_lesson_cd, Exercise.first_exercise)
async def second_lesson_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Lesson.second_lesson)

    await callback.message.delete()
    await callback.message.answer_photo(photo=url_video_class[1],
                                        reply_markup=await lesson_cb.get_kb(await help_functions.get_status(
                                            callback.message.chat.id) == Status.coursing.value, 1))
    await callback.answer()


@router_mini_course.callback_query(F.data == lesson_cb.return_lesson_cd, Lesson.third_lesson)
@router_mini_course.callback_query(F.data == lesson_cb.to_exercise_cd, Lesson.second_lesson)
async def second_exercise_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Exercise.second_exercise)

    await callback.message.delete()
    await callback.message.answer(text=exercise_texts.ex_texts[1],
                                  reply_markup=await exercise_cb.get_exercise_kb(await help_functions.get_status(
                                            callback.message.chat.id) == Status.coursing.value, 1),
                                  disable_web_page_preview=True)
    await callback.answer()


@router_mini_course.callback_query(F.data == exercise_cb.return_exercise_cd, Exercise.third_exercise)
@router_mini_course.callback_query(F.data == exercise_cb.to_lesson_cd, Exercise.second_exercise)
async def third_lesson_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Lesson.third_lesson)

    await callback.message.delete()
    await callback.message.answer_photo(photo=url_video_class[2],
                                        reply_markup=await lesson_cb.get_kb(await help_functions.get_status(
                                            callback.message.chat.id) == Status.coursing.value, 2))
    await callback.answer()


@router_mini_course.callback_query(F.data == lesson_cb.return_lesson_cd, Lesson.fourth_lesson)
@router_mini_course.callback_query(F.data == lesson_cb.to_exercise_cd, Lesson.third_lesson)
async def third_exercise_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Exercise.third_exercise)

    await callback.message.delete()
    await callback.message.answer(text=exercise_texts.ex_texts[2],
                                  reply_markup=await exercise_cb.get_exercise_kb(await help_functions.get_status(
                                            callback.message.chat.id) == Status.coursing.value, 2),
                                  disable_web_page_preview=True)
    await callback.answer()


@router_mini_course.callback_query(F.data == exercise_cb.return_exercise_cd, Exercise.fourth_exercise)
@router_mini_course.callback_query(F.data == exercise_cb.to_lesson_cd, Exercise.third_exercise)
async def fourth_lesson_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Lesson.fourth_lesson)

    await callback.message.delete()
    await callback.message.answer_photo(photo=url_video_class[3],
                                        reply_markup=await lesson_cb.get_kb(await help_functions.get_status(
                                            callback.message.chat.id) == Status.coursing.value, 3))
    await callback.answer()


@router_mini_course.callback_query(F.data == lesson_cb.return_lesson_cd, Lesson.fifth_lesson)
@router_mini_course.callback_query(F.data == lesson_cb.to_exercise_cd, Lesson.fourth_lesson)
async def fourth_exercise_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Exercise.fourth_exercise)

    await callback.message.delete()
    await callback.message.answer(text=exercise_texts.ex_texts[3],
                                  reply_markup=await exercise_cb.get_exercise_kb(await help_functions.get_status(
                                            callback.message.chat.id) == Status.coursing.value, 2),
                                  disable_web_page_preview=True)
    await callback.answer()


@router_mini_course.callback_query(F.data == exercise_cb.return_exercise_cd, Exercise.fifth_exercise)
@router_mini_course.callback_query(F.data == exercise_cb.to_lesson_cd, Exercise.fourth_exercise)
async def fifth_lesson_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Lesson.fifth_lesson)

    await callback.message.delete()
    await callback.message.answer_photo(photo=url_video_class[4],
                                        reply_markup=await lesson_cb.get_kb(await help_functions.get_status(
                                            callback.message.chat.id) == Status.coursing.value, 4))
    await callback.answer()


@router_mini_course.callback_query(F.data == lesson_cb.return_lesson_cd, Lesson.sixth_lesson)
@router_mini_course.callback_query(F.data == lesson_cb.to_exercise_cd, Lesson.fifth_lesson)
async def fifth_exercise_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Exercise.fifth_exercise)

    await callback.message.delete()
    await callback.message.answer(text=exercise_texts.ex_texts[4],
                                  reply_markup=await exercise_cb.get_exercise_kb(await help_functions.get_status(
                                            callback.message.chat.id) == Status.coursing.value, 4),
                                  disable_web_page_preview=True)
    await callback.answer()


@router_mini_course.callback_query(F.data == exercise_cb.return_exercise_cd, Exercise.sixth_exercise)
@router_mini_course.callback_query(F.data == exercise_cb.to_lesson_cd, Exercise.fifth_exercise)
async def sixth_lesson_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Lesson.sixth_lesson)

    await callback.message.delete()
    await callback.message.answer_photo(photo=url_video_class[5],
                                        reply_markup=await lesson_cb.get_kb(await help_functions.get_status(
                                            callback.message.chat.id) == Status.coursing.value, 5))
    await callback.answer()


@router_mini_course.callback_query(F.data == lesson_cb.return_lesson_cd, Lesson.sixth_lesson)
@router_mini_course.callback_query(F.data == lesson_cb.to_exercise_cd, Lesson.sixth_lesson)
async def sixth_exercise_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Exercise.sixth_exercise)

    await callback.message.delete()
    await callback.message.answer(text=exercise_texts.ex_texts[5],
                                  reply_markup=await exercise_cb.get_exercise_kb(await help_functions.get_status(
                                            callback.message.chat.id) == Status.coursing.value, 5),
                                  disable_web_page_preview=True)
    await callback.answer()


@router_mini_course.callback_query(F.data == exercise_cb.to_lesson_cd, Exercise.sixth_exercise)
async def end_class_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Lesson.end_course)

    await callback.message.delete()
    await callback.message.answer_photo(photo=url_intro_exercise[7], caption="Конец!",
                                        reply_markup=lesson_cb.end_course_kb())
    await callback.answer()


@router_mini_course.callback_query(F.data == lesson_cb.end_course_cd, Lesson.end_course)
@router_mini_course.callback_query(F.data == lesson_cb.close_mini_course_cd)
async def close_mini_course(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.admin_default
                          if str(callback.message.chat.id) == ADMIN
                          else UserState.user_default if not await help_functions.get_status(
        callback.message.chat.id) == Status.coursing.value else UserHello.main_info1)

    if (await state.get_state()) == UserHello.main_info1:
        await hello.main_info1(callback, state)
    else:
        await print_menu.print_main_menu_msg(callback.message, state)
    # elif (await state.get_state()) == AdminState.admin_default:
    #     await print_admin_main_menu_handler(callback)
    # else:
    #     await print_user_main_menu_handler(callback)
