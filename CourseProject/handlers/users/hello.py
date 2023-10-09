from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers import help_functions
from kb.user import hello_callback
from models.users import Status
from res.media_files.media_files_id import url_hello, url_after_course
from res.texts.user_texts import hello_texts
from states.user_states import UserHello

router_uh = Router()


async def user_hello(msg: Message, state: FSMContext, user_db):
    if not user_db:
        await help_functions.create_user_db(msg.chat.id, Status.coursing.value)

    await state.set_state(UserHello.hello1)
    await msg.answer_photo(photo=url_hello[0], caption=hello_texts.hello1_text.format(name=msg.from_user.full_name),
                           reply_markup=hello_callback.hello1_kb())


@router_uh.callback_query(F.data == hello_callback.hello_cd, UserHello.hello1)
async def hello_2(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserHello.hello2)

    await callback.message.delete()
    await callback.message.answer_photo(photo=url_hello[1], caption=hello_texts.hello2_text,
                                        reply_markup=hello_callback.hello2_kb())
    await callback.answer()


@router_uh.callback_query(F.data == hello_callback.hello_cd, UserHello.hello2)
async def hello_3(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserHello.hello3)

    await callback.message.delete()
    await callback.message.answer_photo(photo=url_hello[2], caption=hello_texts.hello3_text,
                                        reply_markup=hello_callback.hello3_kb())
    await callback.answer()


async def main_info1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserHello.main_info1)

    await callback.message.delete()
    await callback.message.answer_photo(photo=url_after_course[0],
                                        caption=hello_texts.important_info_text,
                                        reply_markup=hello_callback.main_info1())
    await callback.answer()


@router_uh.callback_query(F.data == hello_callback.main_info_cd, UserHello.main_info1)
async def main_info2(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserHello.main_info2)

    await callback.message.delete()
    await callback.message.answer(text=hello_texts.about_main_menu_text, reply_markup=hello_callback.main_info2())
    await callback.answer()
