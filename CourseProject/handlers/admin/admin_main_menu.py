# from aiogram import types, Router, F
# from aiogram.fsm.context import FSMContext
#
# from core.config import ADMIN
# from handlers.help_functions import get_status
# from kb.admin import main_menu
# from models.users import Status
# from res.texts.admin import main_menu_text
# from kb.feeling_tracker import help_tracker
# from states.admin_states import AdminState, AdminHelpStates
#
# router_amm = Router()
#
#
# @router_amm.callback_query(F.data == help_tracker.about_traker_cd, AdminState.admin_default)
# async def print_admin_main_menu_handler(callback: types.CallbackQuery):
#     try:
#         await callback.message.delete()
#     except Exception:
#         print()
#
#     await callback.message.answer(text=main_menu_text.text, reply_markup=main_menu.get_admin_main_menu_kb(
#         await get_status(callback.message.chat.id)))
#
#     await callback.answer()
#
#
# @router_amm.message(F.text == '/menu')
# async def print_admin_main_menu_msg(message: types.Message, state: FSMContext):
#     try:
#         await message.delete()
#     except Exception:
#         print()
#     if message.chat.id != ADMIN:
#         return
#     cur_state = await state.get_state()
#     if cur_state == AdminHelpStates.help1 or cur_state == AdminHelpStates.help2 or cur_state == AdminHelpStates.help3:
#         return
#
#     await state.set_state(AdminState.admin_default)
#     await message.answer(text=main_menu_text.text, reply_markup=main_menu.get_admin_main_menu_kb(
#         await get_status(message.chat.id)))
