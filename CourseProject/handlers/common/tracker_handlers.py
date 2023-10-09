from datetime import datetime
from enum import Enum

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import insert, select, update

from core.config import ADMIN
from database.database import get_async_session
from kb.feeling_tracker import getting_feelings_kb
from kb.feeling_tracker.getting_feelings_kb import get_felling_describe, return_kb, mood_tracker_main_menu, end_kb
from models.feeling_logs import feeling_logs
from models.users import users
from res.media_files.media_files_id import url_after_course
from states.admin_states import AdminState
from states.feeling_track_states import TrackerStates
from states.user_states import UserState

tracker_router = Router()


class Feelings(Enum):
    joy = getting_feelings_kb.emotion_joy_cd
    calm = getting_feelings_kb.emotion_calm_cd
    fatigue = getting_feelings_kb.emotion_fatigue_cd
    anxiety = getting_feelings_kb.emotion_anxiety_cd
    angry = getting_feelings_kb.emotion_angry_cd
    user_text = getting_feelings_kb.emotion_user_text_cd


feelings_names = ['радость', 'спокойствие', 'усталость', 'тревожность', 'злость', 'напишу сам']
feelings_id = {Feelings.joy.value: 0, Feelings.calm.value: 1, Feelings.fatigue.value: 2,
               Feelings.anxiety.value: 3, Feelings.angry.value: 4,
               Feelings.user_text.value: 5}


@tracker_router.message(F.text == '/tracker')
async def sent_feelings_menu(msg: Message, state: FSMContext):
    await msg.answer_photo(photo=url_after_course[2],
                           caption="Привет, это твой трекер)\nСамое время тренировать свои чувства!"
                                   "\n\nПожалуйста, выбери один из вариантов ниже",
                           reply_markup=mood_tracker_main_menu())


@tracker_router.callback_query(F.data == Feelings.fatigue.value)
@tracker_router.callback_query(F.data == Feelings.anxiety.value)
@tracker_router.callback_query(F.data == Feelings.angry.value)
@tracker_router.callback_query(F.data == Feelings.calm.value)
@tracker_router.callback_query(F.data == Feelings.joy.value)
async def select_feelings(callback: types.CallbackQuery, state: FSMContext):
    async for session in get_async_session():
        async with session.begin():
            user_id = await session.execute(select(users.c.id).where(users.c.user_id == callback.message.chat.id))
            user_id = user_id.first()[0]

            await session.execute(insert(feeling_logs).
                                  values(user_id=user_id, date=datetime.now().date(),
                                         feeling_id=feelings_id[callback.data],
                                         feeling_str=feelings_names[feelings_id[callback.data]]))
            await session.commit()

    await state.set_state(TrackerStates.choose_feeling)

    await callback.message.delete()
    await callback.message.answer_photo(photo=url_after_course[3],
                                        caption=f'<b>Ты чувствуешь:</b> {feelings_names[feelings_id[callback.data]]}\n'
                                                f'Хочешь поделиться чем-то еще?',
                                        reply_markup=get_felling_describe())


@tracker_router.callback_query(F.data == Feelings.user_text.value)
async def user_text_feelings(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(TrackerStates.get_user_text_feeling)
    await callback.message.delete()
    data = {'calldel': await callback.message.answer_photo(photo=url_after_course[1],
                                        caption="Напишите нам свое чувство)\n\nЕсли что, после этого шага,"
                                                " вы сможете расписать его поподробнее",
                                        reply_markup=return_kb())}
    await state.set_data(data)

    await callback.answer()


@tracker_router.callback_query(F.data == 'return_cd', TrackerStates.get_user_text_feeling)
async def return_to_feeling_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(TrackerStates.choose_feeling)
    await callback.message.delete()
    await callback.message.answer_photo(photo=url_after_course[2],
                                        caption="Самое время чувствовать)",
                                        reply_markup=mood_tracker_main_menu())
    await callback.answer()


@tracker_router.message(F.text, TrackerStates.get_user_text_feeling)
async def get_user_text_feeling(msg: Message, state: FSMContext):
    cd = await state.get_data()
    await delete_cb(cd['calldel'])
    await state.clear_data()

    await state.set_state(TrackerStates.got_user_text_feeling)
    async for session in get_async_session():
        async with session.begin():
            user_id = await session.execute(select(users.c.id).where(users.c.user_id == msg.chat.id))
            user_id = user_id.first()[0]

            await session.execute(
                insert(feeling_logs).values(user_id=user_id, date=datetime.now().date(), feeling_id=5,
                                            feeling_str=msg.text))
            await session.commit()

    await msg.delete()
    await msg.answer_photo(photo=url_after_course[3],
                           caption=f'<b>Ты чувствуешь:</b> {msg.text}\nХочешь поделиться чем-то еще?',
                           reply_markup=get_felling_describe())


async def delete_cb(cb: types.Message):
    await cb.delete()


@tracker_router.callback_query(F.data == 'end_cd', TrackerStates.get_describe_text)
@tracker_router.callback_query(F.data == 'skip_describe_cd', TrackerStates.choose_feeling)
@tracker_router.callback_query(F.data == 'skip_describe_cd', TrackerStates.got_user_text_feeling)
async def skip_description(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(
        AdminState.admin_default if str(callback.message.chat.id) == ADMIN else UserState.user_default)
    async for session in get_async_session():
        async with session.begin():
            user_id = await session.execute(select(users.c.id).where(users.c.user_id == callback.message.chat.id))
            user_id = user_id.first()[0]
            ex_txt = await session.execute(select(feeling_logs.c.feeling_str).where(
                feeling_logs.c.user_id == user_id and feeling_logs.c.date == datetime.today()))
            ex_txt = ex_txt.first()[0]
            await session.commit()

    await callback.message.delete()
    await callback.message.answer_photo(photo=url_after_course[3],
                                        caption=f'<b>Ты чувствуешь:</b> {ex_txt}\n\n')
    await callback.message.answer(text=f'На сегодня все)\nТы умничка!')
    await callback.answer()


@tracker_router.callback_query(F.data == 'sup_describe_cd', TrackerStates.choose_feeling)
@tracker_router.callback_query(F.data == 'sup_describe_cd', TrackerStates.got_user_text_feeling)
async def do_describe_feeling(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(TrackerStates.get_describe_text)

    await callback.message.delete()
    data = {'calldel': await callback.message.answer_photo(photo=url_after_course[3],
                                        caption=f'Мы не ограничиваем себя и не хотим ограничевать тебя)\n\nДополни свой ответ',
                                        reply_markup=end_kb())}
    await state.set_data(data)
    await callback.answer()


@tracker_router.message(F.text, TrackerStates.get_describe_text)
async def get_describe_feeling(msg: Message, state: FSMContext):
    cd = await state.get_data()
    await delete_cb(cd['calldel'])
    await state.clear_data()

    await state.set_state(AdminState.admin_default if str(msg.chat.id) == ADMIN else UserState.user_default)
    async for session in get_async_session():
        async with session.begin():
            user_id = await session.execute(select(users.c.id).where(users.c.user_id == msg.chat.id))
            user_id = user_id.first()[0]
            ex_txt = await session.execute(
                select(feeling_logs.c.feeling_str).where(feeling_logs.c.user_id == int(user_id)))
            ex_txt = ex_txt.first()[0]

            await session.execute(
                update(feeling_logs).where(feeling_logs.c.user_id == int(user_id)).values(describe=msg.text))
            await session.commit()

    await msg.delete()
    await msg.answer_photo(photo=url_after_course[3],
                           caption=f'<b>Ты чувствуешь:</b> {ex_txt}\n'
                                   f'<b>Ты дополнил ответ:</b> {msg.text}')

    await msg.answer(text='На сегодня все)\nТы умничка!')
