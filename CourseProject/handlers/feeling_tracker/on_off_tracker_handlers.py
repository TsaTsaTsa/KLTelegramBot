from typing import List

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_media_group import media_group_handler
from sqlalchemy import update

from database.database import get_async_session
from handlers.common import print_menu
from kb.admin import main_menu
from kb.admin.callback import on_off_feeling_tracker_kb, yes_cd, no_cd
from models.users import users, Status
from states.admin_states import AdminState
from states.feeling_track_states import OnOffStates
from states.user_states import UserState

on_off_tracker_router = Router()


@on_off_tracker_router.callback_query(F.data == main_menu.to_on_feeling_tracker_cd, UserState.user_default)
@on_off_tracker_router.callback_query(F.data == main_menu.to_on_feeling_tracker_cd, AdminState.admin_default)
async def to_on_feeling_tracker(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(OnOffStates.to_on_state)
    await callback.message.edit_text(text="Хотите включить трекер чувств?", reply_markup=on_off_feeling_tracker_kb())

    await callback.answer()


@on_off_tracker_router.callback_query(F.data == main_menu.to_off_feeling_tracker_cd, UserState.user_default)
@on_off_tracker_router.callback_query(F.data == main_menu.to_off_feeling_tracker_cd, AdminState.admin_default)
async def to_off_feeling_tracker(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(OnOffStates.to_off_state)
    await callback.message.edit_text(text="Хотите выключить трекер чувств?", reply_markup=on_off_feeling_tracker_kb())

    await callback.answer()


@on_off_tracker_router.callback_query(F.data == yes_cd, OnOffStates.to_on_state)
async def on_feeling_tracker(callback: types.CallbackQuery, state: FSMContext):
    async for session in get_async_session():
        async with session.begin():
            await session.execute(
                update(users).where(users.c.user_id == callback.from_user.id).values(
                    status=Status.on_feeling_tracker.value))
            await session.commit()

    try:
        await callback.message.delete()
    except Exception:
        pass
    await callback.message.answer(text="Ты включил трекер чувств)")
    await callback.answer()

    await print_menu.print_main_menu_msg(callback.message, state)


@on_off_tracker_router.callback_query(F.data == yes_cd, OnOffStates.to_off_state)
async def off_feeling_tracker(callback: types.CallbackQuery, state: FSMContext):
    async for session in get_async_session():
        async with session.begin():
            await session.execute(
                update(users).where(users.c.user_id == callback.from_user.id).values(
                    status=Status.off_feeling_tracker.value))
            await session.commit()

    await callback.message.edit_text(text="Ты выключил трекер чувств(")
    await callback.answer()

    await print_menu.print_main_menu_msg(callback.message, state)


@on_off_tracker_router.callback_query(F.data == no_cd, OnOffStates.to_on_state)
@on_off_tracker_router.callback_query(F.data == no_cd, OnOffStates.to_off_state)
async def inactivate_feeling_tracker(callback: types.CallbackQuery, state: FSMContext):
    await print_menu.print_main_menu_msg(callback.message, state)


async def del_callback(del_list: list):
    for cl in del_list:
        try:
            await cl.delete()
        except Exception:
            pass
    del_list.clear()


@on_off_tracker_router.message(AdminState.activate_feeling_track)
@on_off_tracker_router.message(AdminState.inactivate_feeling_track)
@media_group_handler
async def delete_incorrect_data(messages: List[Message]):
    await del_callback(messages)
