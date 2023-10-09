import asyncio

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from core.config import ADMIN
from handlers.help_functions import get_status
from kb import admin, user
from kb.feeling_tracker import help_tracker
from models.users import Status
from res.texts import admin, user_texts
from states.admin_states import AdminState
from states.user_states import UserState

router_mm = Router()
text_ = "Вот такое у нас главное меню"


@router_mm.message(F.text == '/menu')
async def print_main_menu_msg(message: types.Message, state: FSMContext):
    try:
        await message.delete()
    except Exception:
        pass

    status = await get_status(message.chat.id)

    if status is None or status == Status.coursing.value:
        new_msg = await message.answer(text="Меню пока не доступно(")
        await asyncio.sleep(5)
        try:
            await new_msg.delete()
        except Exception:
            pass
        return

    if str(message.chat.id) == ADMIN:
        await state.set_state(AdminState.admin_default)

        await message.answer(text=text_, reply_markup=admin.main_menu.get_admin_main_menu_kb(
            await get_status(message.chat.id)))

    else:
        await state.set_state(UserState.user_default)
        await message.answer(text=text_,
                             reply_markup=user.main_menu_callback.get_user_main_menu_kb(
                                 await get_status(message.chat.id)))


@router_mm.callback_query(F.data == help_tracker.about_traker_cd, AdminState.admin_default)
@router_mm.callback_query(F.data == help_tracker.about_traker_cd, UserState.user_default)
async def print_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except Exception:
        pass

    if str(callback.message.chat.id) == ADMIN:
        await state.set_state(AdminState.admin_default)

        await callback.message.answer(text=text_, reply_markup=admin.main_menu.get_admin_main_menu_kb(
            await get_status(callback.message.chat.id)))

    else:
        await state.set_state(UserState.user_default)
        await callback.message.answer(text=text_,
                             reply_markup=user.main_menu_callback.get_user_main_menu_kb(
                                 await get_status(callback.message.chat.id)))
