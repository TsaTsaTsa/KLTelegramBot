from typing import List

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_media_group import media_group_handler

from handlers import help_functions
from handlers.common import print_menu
from kb.admin import hello_callback
from models.users import Status
from res.texts.admin import admin_help_text
from states.admin_states import AdminHelpStates

router_ah = Router()


async def admin_hello(msg: Message, state: FSMContext, user_db):
    if not user_db:
        await help_functions.create_user_db(msg.chat.id, Status.off_feeling_tracker.value)
        await help1_handlers(msg, state)
    else:
        await print_menu.print_main_menu_msg(msg, state)


async def help1_handlers(msg: Message, state: FSMContext):
    await state.set_state(AdminHelpStates.help1)

    await msg.answer(text=admin_help_text.text1.format(name=msg.from_user.full_name),
                     reply_markup=hello_callback.help_kb())


@router_ah.callback_query(F.data == hello_callback.help_cd, AdminHelpStates.help1)
async def help2_handlers(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminHelpStates.help2)

    await callback.message.edit_text(text=admin_help_text.text2, reply_markup=hello_callback.next_kb())
    await callback.answer()


@router_ah.callback_query(F.data == hello_callback.next_cd, AdminHelpStates.help2)
async def help3_handlers(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminHelpStates.help3)

    await callback.message.edit_text(text=admin_help_text.text3, reply_markup=hello_callback.next_kb())
    await callback.answer()


async def del_callback(del_list: list):
    for cl in del_list:
        await cl.delete()
    del_list.clear()


@router_ah.message(AdminHelpStates.help1)
@router_ah.message(AdminHelpStates.help2)
@router_ah.message(AdminHelpStates.help3)
@media_group_handler
async def delete_incorrect_data(messages: List[Message]):
    await del_callback(messages)
