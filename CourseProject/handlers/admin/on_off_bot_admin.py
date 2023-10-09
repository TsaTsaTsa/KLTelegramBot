from aiogram import Router, F, types
from aiogram.types import Message
from sqlalchemy import update

from database.database import get_async_session
from handlers.common.exercise_handelrs import get_reply
from handlers.help_functions import get_status
from kb.admin.deactivate_bot_callback import yeas_no_kb, yes_cd, no_cd
from kb.admin.main_menu import deactivate_bot_cd, get_deactivate_admin_main_menu_kb, activate_bot_cd, \
    get_admin_main_menu_kb
from models.users import users, Status
from states.admin_states import AdminState

on_off_bot_admin_router = Router()


async def delete_callback_list(del_list: list):
    for cl in del_list:
        await delete_callback(cl)


async def delete_callback(msg: Message):
    try:
        await msg.delete()
    except Exception:
            pass


@on_off_bot_admin_router.callback_query(F.data == deactivate_bot_cd, AdminState.admin_default)
async def ask_deactivate_bot(callback: types.CallbackQuery):
    await delete_callback(callback.message)
    await callback.message.answer(
        text="Уверен, что хочешь отключить рассылку и трекер чувств?\n\nPS: мы сохраним все-все и ты сможешь всегда вернуться к нам",
        reply_markup=yeas_no_kb())
    await callback.answer()


@on_off_bot_admin_router.callback_query(F.data == yes_cd, AdminState.admin_default)
async def deactivate_bot(callback: types.CallbackQuery):
    await delete_callback(callback.message)

    await callback.message.answer(text="Мы будем скучать!(\n\nТеперь твое меню выглядит так",
                                  reply_markup=get_deactivate_admin_main_menu_kb())
    await callback.answer()

    async for session in get_async_session():
        async with session.begin():
            await session.execute(
                update(users).where(users.c.user_id == callback.from_user.id).values(status=Status.inactive.value))
            await session.commit()


@on_off_bot_admin_router.callback_query(F.data == no_cd, AdminState.admin_default)
async def dont_deactivate_bot(callback: types.CallbackQuery):
    await delete_callback(callback.message)

    reply = await get_reply(callback.from_user.id)

    await callback.message.answer(text="Мы ценим, что вы с нами!)", reply_markup=reply)
    await callback.answer()


@on_off_bot_admin_router.callback_query(F.data == activate_bot_cd, AdminState.admin_default)
async def activate_bot(callback: types.CallbackQuery):
    await delete_callback(callback.message)

    async for session in get_async_session():
        async with session.begin():
            await session.execute(
                update(users).where(users.c.user_id == callback.from_user.id).values(
                    status=Status.off_feeling_tracker.value))
            await session.commit()

    await callback.message.answer(text="Ура, рады что вы вернулись!",
                                  reply_markup=get_admin_main_menu_kb(await get_status(callback.message.chat.id)))
    await callback.answer()
