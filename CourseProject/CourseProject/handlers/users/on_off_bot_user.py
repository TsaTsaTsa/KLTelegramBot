from aiogram import Router, F, types
from sqlalchemy import update

from database.database import get_async_session
from handlers.common.exercise_handelrs import get_reply
from handlers.help_functions import get_status
from kb.admin.deactivate_bot_callback import yeas_no_kb, yes_cd, no_cd
from kb.admin.main_menu import deactivate_bot_cd, activate_bot_cd
from kb.user.main_menu_callback import get_user_deactivate_main_menu_kb, get_user_main_menu_kb
from models.users import users, Status
from states.user_states import UserState

on_off_bot_user_router = Router()


@on_off_bot_user_router.callback_query(F.data == deactivate_bot_cd, UserState.user_default)
async def ask_deactivate_bot(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        text="Уверен, что хочешь отключить рассылку и трекер чувств?\n\nPS: мы сохраним все-все и ты сможешь всегда вернуться к нам",
        reply_markup=yeas_no_kb())
    await callback.answer()


@on_off_bot_user_router.callback_query(F.data == yes_cd, UserState.user_default)
async def deactivate_bot(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text="Мы будем скучать!(\n\nТеперь твое меню выглядит так",
                                  reply_markup=get_user_deactivate_main_menu_kb())
    await callback.answer()

    async for session in get_async_session():
        async with session.begin():
            await session.execute(
                update(users).where(users.c.user_id == callback.from_user.id).values(status=Status.inactive.value))
            await session.commit()


@on_off_bot_user_router.callback_query(F.data == no_cd, UserState.user_default)
async def dont_deactivate_bot(callback: types.CallbackQuery):
    await callback.message.delete()
    reply = await get_reply(callback.from_user.id)

    await callback.message.answer(text="Мы ценим, что вы с нами!)", reply_markup=reply)
    await callback.answer()


@on_off_bot_user_router.callback_query(F.data == activate_bot_cd, UserState.user_default)
async def activate_bot(callback: types.CallbackQuery):
    await callback.message.delete()

    async for session in get_async_session():
        async with session.begin():
            await session.execute(
                update(users).where(users.c.user_id == callback.from_user.id).values(
                    status=Status.off_feeling_tracker.value))
            await session.commit()

    await callback.message.answer(text="Ура, рады что вы вернулись!",
                                  reply_markup=get_user_main_menu_kb(await get_status(callback.message.chat.id)))
    await callback.answer()
