from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from sqlalchemy import update

from core.config import ADMIN
from database.database import get_async_session
from kb import admin
from kb import user
from kb.feeling_tracker import help_tracker
from models.users import Status, users
from res.media_files.media_files_id import url_about_tracker
from res.texts.feeling_tracker import about_tracker
from states.admin_states import AdminHelpStates, AdminState
from states.feeling_track_states import FeelingHelpStates
from states.user_states import UserState, UserHello

router_ht = Router()


@router_ht.callback_query(F.data == admin.hello_callback.next_cd, AdminHelpStates.help3)
@router_ht.callback_query(F.data == user.hello_callback.main_info_cd, UserHello.main_info2)
async def about_tracker_handler1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(FeelingHelpStates.help1)

    await callback.message.delete()
    await callback.message.answer_photo(photo=url_about_tracker[0], caption=about_tracker.text1,
                                        reply_markup=help_tracker.about_traker_kb())
    await callback.answer()


@router_ht.callback_query(F.data == help_tracker.about_traker_cd, FeelingHelpStates.help1)
async def about_tracker_handler2(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(FeelingHelpStates.help2)

    await callback.message.delete()
    await callback.message.answer_photo(photo=url_about_tracker[1], caption=about_tracker.text2,
                                        reply_markup=help_tracker.about_traker_kb())
    await callback.answer()


@router_ht.callback_query(F.data == help_tracker.about_traker_cd, FeelingHelpStates.help2)
async def about_tracker_handler3(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(FeelingHelpStates.help3)

    await callback.message.delete()
    await callback.message.answer_photo(photo=url_about_tracker[2], caption=about_tracker.text3,
                                        reply_markup=help_tracker.about_traker_kb())
    await callback.answer()


@router_ht.callback_query(F.data == help_tracker.about_traker_cd, FeelingHelpStates.help3)
async def get_skip_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(FeelingHelpStates.get_skip)

    await callback.message.delete()
    await callback.message.answer_photo(photo=url_about_tracker[3], caption=about_tracker.text4,
                                        reply_markup=help_tracker.get_skip_tracker_kb())
    await callback.answer()


@router_ht.callback_query(F.data == help_tracker.get_tracker_cd, FeelingHelpStates.get_skip)
@router_ht.callback_query(F.data == help_tracker.skip_tracker_cd, FeelingHelpStates.get_skip)
async def update_user_status_handler(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == help_tracker.get_tracker_cd:
        new_user_status = Status.on_feeling_tracker.value
    else:
        new_user_status = Status.off_feeling_tracker.value

    async for session in get_async_session():
        async with session.begin():
            await session.execute(
                update(users).where(users.c.user_id == callback.from_user.id).values(status=new_user_status))
            await session.commit()

    await end_help_handler(callback, state)


async def end_help_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(AdminState.admin_default
                          if str(callback.message.chat.id) == ADMIN
                          else UserState.user_default)

    await callback.message.answer_photo(photo=url_about_tracker[4], caption=about_tracker.end_text,
                                        reply_markup=help_tracker.end_help_kb())
    await callback.answer()


