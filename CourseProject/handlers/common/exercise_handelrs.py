from datetime import datetime

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, update

from core.config import ADMIN
from database.database import get_async_session
from handlers.help_functions import print_post
from kb.admin.main_menu import get_admin_main_menu_kb, do_not_exercises_cd, all_exercises_cd
from kb.exrcises_cb.exercises_callback import exercise_back_done_kb, exercise_forward_back_done_kb, \
    exercise_forward_done_kb, exercise_done_kb, exercise_back_undone_kb, exercise_forward_back_undone_kb, \
    exercise_forward_undone_kb, exercise_undone_kb, select_done_cd, select_undone_cd, exercise_forward_cd, \
    exercise_back_cd, exercise_close_cd
from kb.user.main_menu_callback import get_user_main_menu_kb
from models.exercises_logs import exercise_logs
from models.users import users
from states.admin_states import AdminState
from states.user_states import UserState

exercise_router = Router()

mesg_to_delete = 'mesg_to_delete'
is_list_undone = 'is_list_undone'
exercise_list = 'exercise_list'
done_exercises_id = 'done_exercises_id'
cur_num = 'cur_num'


async def update_exercise_status(is_done_: bool, state: FSMContext):
    exercises_list = list((await state.get_data())[exercise_list])
    cur_exercise_num = int((await state.get_data())[cur_num])
    cur_exercise = exercises_list[cur_exercise_num]

    async for session in get_async_session():
        async with session.begin():
            date_ = cur_exercise[3]

            if date_.month != datetime.today().month:
                await session.execute(
                    update(exercise_logs).where(exercise_logs.c.id == int(cur_exercise[0])).values(is_done=is_done_,
                                                                                                   is_done_last_month=(
                                                                                                       not is_done_),
                                                                                                   date_change_status=datetime.now().date()))
            else:
                await session.execute(
                    update(exercise_logs).where(exercise_logs.c.id == int(cur_exercise[0])).values(is_done=is_done_,
                                                                                                   date_change_status=datetime.now().date()))
            await session.commit()


@exercise_router.callback_query(F.data == select_done_cd, UserState.forward_back_callback)
@exercise_router.callback_query(F.data == select_done_cd, UserState.forward_callback)
@exercise_router.callback_query(F.data == select_done_cd, UserState.back_callback)
@exercise_router.callback_query(F.data == select_done_cd, UserState.undone_callback)
async def select_done(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    exercise_list_ = list((await state.get_data())[exercise_list])
    cur_exercise_num = int((await state.get_data())[cur_num])
    old_done_exercise_id_list = list((await state.get_data())[done_exercises_id])
    old_done_exercise_id_list.append(exercise_list_[cur_exercise_num][0])
    await state.update_data(done_exercises_id=old_done_exercise_id_list)

    if current_state == UserState.back_callback:
        reply = exercise_back_done_kb()
    elif current_state == UserState.forward_back_callback:
        reply = exercise_forward_back_done_kb()
    elif current_state == UserState.forward_callback:
        reply = exercise_forward_done_kb()
    else:
        reply = exercise_done_kb()

    await callback.message.edit_reply_markup(reply_markup=reply)

    await update_exercise_status(True, state)


@exercise_router.callback_query(F.data == select_undone_cd, UserState.forward_back_callback)
@exercise_router.callback_query(F.data == select_undone_cd, UserState.forward_callback)
@exercise_router.callback_query(F.data == select_undone_cd, UserState.back_callback)
@exercise_router.callback_query(F.data == select_undone_cd, UserState.done_callback)
async def select_exercise_undone(callback: types.CallbackQuery, state: FSMContext):
    exercise_list_ = list((await state.get_data())[exercise_list])
    cur_exercise_num = int((await state.get_data())[cur_num])
    old_done_exercise_id_list = list((await state.get_data())[done_exercises_id])
    old_done_exercise_id_list.remove(exercise_list_[cur_exercise_num][0])
    await state.update_data(done_exercises_id=old_done_exercise_id_list)

    current_state = await state.get_state()

    if current_state == UserState.back_callback:
        reply = exercise_back_undone_kb()
    elif current_state == UserState.forward_back_callback:
        reply = exercise_forward_back_undone_kb()
    elif current_state == UserState.forward_callback:
        reply = exercise_forward_undone_kb()
    else:
        reply = exercise_undone_kb()
    await callback.message.edit_reply_markup(reply_markup=reply)

    await update_exercise_status(False, state)


@exercise_router.callback_query(F.data == all_exercises_cd, UserState.user_default)
@exercise_router.callback_query(F.data == all_exercises_cd, AdminState.admin_default)
async def select_exercise_all(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.get_exercise)
    async for session in get_async_session():
        async with session.begin():
            await state.update_data(is_list_undone=False)

            exercises_list_ = await get_exercise_list(callback.message.chat.id, state)
            done_exercises_id_ = await session.execute(
                select(exercise_logs.c.id).where(exercise_logs.c.is_done == True))
            done_exercises_id_ = done_exercises_id_.fetchall()
            done_exercises_id_ = [e[0] for e in done_exercises_id_]

            await session.commit()
            await state.update_data(exercise_list=exercises_list_)
            await state.update_data(done_exercises_id=done_exercises_id_)
            await state.update_data(cur_num=0)
            await state.update_data(mesg_to_delete=[])

            await callback.message.delete()

            if len(exercises_list_) == 0:
                await state.set_state(
                    AdminState.admin_default if callback.from_user.id == int(ADMIN) else UserState.user_default)
                await callback.message.answer(text="Упс, упражнений еще нет... \nЗначит скоро появятся!",
                                              reply_markup=await get_reply(callback.from_user.id))
                await callback.answer()
                return

            if exercises_list_[0][4]:
                reply = exercise_forward_done_kb()
                if len(exercises_list_) == 1:
                    reply = exercise_done_kb()
            else:
                reply = exercise_forward_undone_kb()
                if len(exercises_list_) == 1:
                    reply = exercise_undone_kb()

            await state.set_state(UserState.forward_callback)
            msg_to_delete = list((await state.get_data())[mesg_to_delete])
            msg_to_delete = await append_mes_to_del(
                await print_post(exercises_list_[0][2], callback.message, reply), msg_to_delete)
            await state.update_data(mesg_to_delete=msg_to_delete)


@exercise_router.callback_query(F.data == do_not_exercises_cd, AdminState.admin_default)
@exercise_router.callback_query(F.data == do_not_exercises_cd, UserState.user_default)
async def select_not_done_exercise(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.get_exercise)

    await state.update_data(is_list_undone=True)
    exercises_list_ = await get_exercise_list(callback.message.chat.id, state)
    done_exercises_id_ = []
    await state.update_data(exercise_list=exercises_list_)
    await state.update_data(done_exercises_id=done_exercises_id_)
    await state.update_data(cur_num=0)
    await state.update_data(mesg_to_delete=[])

    await callback.message.delete()

    if len(exercises_list_) == 0:
        await state.set_state(
            AdminState.admin_default if callback.from_user.id == int(ADMIN) else UserState.user_default)
        await callback.message.answer(text="Упс, упражнений еще нет... \nЗначит скоро появятся!",
                                      reply_markup=await get_reply(callback.from_user.id))
        await callback.answer()
        return
    reply = exercise_forward_undone_kb()
    if len(exercises_list_) == 1:
        reply = exercise_undone_kb()

    await state.set_state(UserState.forward_callback)
    msg_to_delete = list((await state.get_data())[mesg_to_delete])
    msg_to_delete = await append_mes_to_del(
        await print_post(exercises_list_[0][2], callback.message, reply), msg_to_delete)
    await state.update_data(mesg_to_delete=msg_to_delete)


async def del_callback(del_list: list):
    for cl in del_list:
        try:
            await cl.delete()
        except:
            print()


async def append_mes_to_del(callback_id: list, ad_list: list):
    for cl in callback_id:
        if type(cl) is list:
            for cl1 in cl:
                ad_list.append(cl1)
        else:
            ad_list.append(cl)
    return ad_list


@exercise_router.callback_query(F.data == exercise_forward_cd)
async def get_forward_exercise(callback: types.CallbackQuery, state: FSMContext):
    await del_callback((await state.get_data())[mesg_to_delete])
    await state.update_data(mesg_to_delete=[])

    cur_exercise_num = (await state.get_data())[cur_num] + 1
    await state.update_data(cur_num=cur_exercise_num)

    done_exercises_id_list = list((await state.get_data())[done_exercises_id])
    exercises_list = list((await state.get_data())[exercise_list])
    is_cur_exercise_done = exercises_list[cur_exercise_num][0] in done_exercises_id_list

    if is_cur_exercise_done:
        if cur_exercise_num == len(exercises_list) - 1:
            reply = exercise_back_done_kb()
            await state.set_state(UserState.back_callback)
        elif len(exercises_list) - 1 == 0:
            reply = exercise_done_kb()
            await state.set_state(UserState.done_callback)
        else:
            reply = exercise_forward_back_done_kb()
            await state.set_state(UserState.forward_back_callback)
    else:
        if cur_exercise_num == len(exercises_list) - 1:
            reply = exercise_back_undone_kb()
            await state.set_state(UserState.back_callback)
        elif len(exercises_list) - 1 == 0:
            reply = exercise_undone_kb()
            await state.set_state(UserState.undone_callback)
        else:
            reply = exercise_forward_back_undone_kb()
            await state.set_state(UserState.forward_back_callback)

    msg_to_delete = list((await state.get_data())[mesg_to_delete])
    msg_to_delete = await append_mes_to_del(
        await print_post(exercises_list[cur_exercise_num][2], callback.message, reply_markup=reply), msg_to_delete)
    await state.update_data(mesg_to_delete=msg_to_delete)


@exercise_router.callback_query(F.data == exercise_back_cd)
async def get_back_exercise(callback: types.CallbackQuery, state: FSMContext):
    await del_callback((await state.get_data())[mesg_to_delete])
    await state.update_data(mesg_to_delete=[])

    cur_exercise_num = (await state.get_data())[cur_num] - 1
    await state.update_data(cur_num=cur_exercise_num)

    done_exercises_id_list = list((await state.get_data())[done_exercises_id])
    exercises_list = list((await state.get_data())[exercise_list])
    is_cur_exercise_done = exercises_list[cur_exercise_num][0] in done_exercises_id_list

    if is_cur_exercise_done:
        if cur_exercise_num == 0:
            reply = exercise_forward_done_kb()
            await state.set_state(UserState.forward_callback)
        elif len(exercises_list) - 1 == 0:
            reply = exercise_done_kb()
            await state.set_state(UserState.done_callback)
        else:
            reply = exercise_forward_back_done_kb()
            await state.set_state(UserState.forward_back_callback)
    else:
        if cur_exercise_num == 0:
            reply = exercise_forward_undone_kb()
            await state.set_state(UserState.forward_callback)
        elif len(exercises_list) - 1 == 0:
            reply = exercise_undone_kb()
            await state.set_state(UserState.undone_callback)
        else:
            reply = exercise_forward_back_undone_kb()
            await state.set_state(UserState.forward_back_callback)

    msg_to_delete = list((await state.get_data())[mesg_to_delete])
    msg_to_delete = await append_mes_to_del(await print_post(exercises_list[cur_exercise_num][2], callback.message, reply_markup=reply), msg_to_delete)
    await state.update_data(mesg_to_delete=msg_to_delete)


@exercise_router.callback_query(F.data == exercise_close_cd)
async def exercise_close(callback: types.CallbackQuery, state: FSMContext):
    await del_callback((await state.get_data())[mesg_to_delete])
    await state.clear_data()
    reply = await get_reply(callback.from_user.id)

    await state.set_state(AdminState.admin_default if callback.from_user.id == int(ADMIN) else UserState.user_default)
    await callback.message.answer(text="Меню от нас для вас)", reply_markup=reply)
    await callback.answer()


async def get_reply(us_id: int):
    async for session in get_async_session():
        async with session.begin():
            user_status = await session.execute(
                select(users.c.status).where(users.c.user_id == us_id))
            await session.commit()
            user_status = user_status.first()[0]

    if us_id == int(ADMIN):
        return get_admin_main_menu_kb(user_status)
    return get_user_main_menu_kb(user_status)


async def get_exercise_list(u_id: int, state: FSMContext):
    async for session in get_async_session():
        async with session.begin():
            if not ((await state.get_data())[is_list_undone]):
                exercises = await session.execute(
                    select(exercise_logs).
                    where(exercise_logs.c.user_id == u_id).
                    order_by(exercise_logs.c.id))
            else:
                exercises = await session.execute(
                    select(exercise_logs).
                    where(
                        exercise_logs.c.user_id == u_id).
                    where(
                        exercise_logs.c.is_done == False).
                    order_by(
                        exercise_logs.c.id))
            await session.commit()

            return exercises.fetchall()
