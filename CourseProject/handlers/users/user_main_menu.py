# from aiogram import types, Router, F
# from aiogram.fsm.context import FSMContext
#
# from core.config import ADMIN
# from handlers.help_functions import get_status
# from kb.feeling_tracker import help_tracker
# from kb.user import main_menu_callback
# from kb.user.main_menu_callback import get_user_main_menu_kb
# from models.users import Status
# from res.texts.user_texts import main_menu_text
# from states.user_states import UserState
#
# router_umm = Router()
# text1 = "Вот такое у нас главное меню"
#
#
# @router_umm.callback_query(F.data == help_tracker.about_traker_cd, UserState.user_default)
# async def print_user_main_menu_handler(callback: types.CallbackQuery):
#     try:
#         await callback.message.delete()
#     except Exception:
#         print()
#
#     await callback.message.answer(text=text1, reply_markup=main_menu_callback.get_user_main_menu_kb(
#         await get_status(callback.message.chat.id)))
#
#     await callback.answer()
#
#
# @router_umm.message(F.text == '/menu')
# async def print_user_main_menu_msg(message: types.Message, state: FSMContext):
#     try:
#         await message.delete()
#     except Exception:
#         print()
#     if message.chat.id == ADMIN:
#         return
#     cur_state = await state.get_state()
#
#     await state.set_state(UserState.user_default)
#     await message.answer(text=main_menu_text.text, reply_markup=get_user_main_menu_kb(
#         await get_status(message.chat.id)))
#
