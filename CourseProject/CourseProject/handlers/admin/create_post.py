from typing import List

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_media_group import media_group_handler
from sqlalchemy import insert, select, update
from aiogram import types

import text
from database.database import get_async_session
from handlers.common import print_menu
from handlers.help_functions import print_post, get_status
from kb.admin import main_menu
from kb.admin.callback import get_admin_new_post_menu_kb, add_text_cd, \
    get_admin_add_photo_menu_kb, return_cd, skip_text_cd, \
    add_photo_text_cd, end_create_post_text_cd, return_kb
from kb.admin.learning_sections_callback import learning_sections_buttons, SectionsNames, SectionsCd, SectionsId
from kb.admin.main_menu import create_exercise_cd, create_post_cd
from models.posts import posts
from models.photo import photos
from models.users import users
from states.admin_states import AdminState

router_admin = Router()
msg_delete = 'msg_delete'
is_ex = 'is_ex'
new_post_id = 'new_post_id'
sections = 'sections'


@router_admin.callback_query(F.data == return_cd, AdminState.choose_section)
async def return_to_main(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.admin_default)
    await callback.message.delete()

    await print_menu.print_main_menu_msg(callback.message, state)


@router_admin.callback_query(F.data == return_cd, AdminState.create_post)
@router_admin.callback_query(F.data == create_exercise_cd, AdminState.admin_default)
@router_admin.callback_query(F.data == create_post_cd, AdminState.admin_default)
async def add_post(callback: types.CallbackQuery, state: FSMContext):
    await state.clear_data()
    await state.update_data(is_ex=callback.data == create_exercise_cd)
    await state.update_data(new_post_id={})
    await state.update_data(msg_delete={})
    await state.update_data(sections="")

    await state.set_state(AdminState.choose_section)
    if callback.data == create_exercise_cd:
        await callback.message.edit_text(text="Ура-ура, новое упражнение!\n\n Давайте выберем тему упражнения)",
                                         reply_markup=learning_sections_buttons())
    else:
        await callback.message.edit_text(text="Ура-ура, новый пост!\n\n Давайте выберем тему поста)",
                                         reply_markup=learning_sections_buttons())
    await callback.answer()


@router_admin.callback_query(F.data == SectionsCd.method_demidov_cd.value, AdminState.choose_section)
@router_admin.callback_query(F.data == SectionsCd.method_knebel_cd.value, AdminState.choose_section)
@router_admin.callback_query(F.data == SectionsCd.method_stanislavsky_cd.value, AdminState.choose_section)
@router_admin.callback_query(F.data == SectionsCd.method_chekhov_cd.value, AdminState.choose_section)
@router_admin.callback_query(F.data == SectionsCd.meditation_cd.value, AdminState.choose_section)
@router_admin.callback_query(F.data == SectionsCd.quality_cd.value, AdminState.choose_section)
@router_admin.callback_query(F.data == SectionsCd.another_cd.value, AdminState.choose_section)
async def add_post(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(sections=callback.data)
    await state.set_state(AdminState.create_post)
    await callback.message.edit_text(text=f"Вы выбрали категорию: <b>{SectionsNames[callback.data[:-3]].value}</b>"
                                          f"\n\n Давай дальше: будет ли текст?")
    await callback.message.edit_reply_markup(reply_markup=get_admin_new_post_menu_kb())
    await callback.answer()


@router_admin.callback_query(F.data == add_text_cd, AdminState.create_post)
async def admin_add_text(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.send_text)
    mes_to_delete = list((await state.get_data())[msg_delete])
    mes_to_delete.append(await callback.message.edit_text(text="Ждем текст)", reply_markup=return_kb()))

    await state.update_data(msg_delete=mes_to_delete)
    await callback.answer()


@router_admin.callback_query(F.data == return_cd, AdminState.send_text)
async def return_to_add_text_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.create_post)
    await state.update_data(msg_delete={})

    if (await state.get_data())[is_ex]:
        await callback.message.edit_text(text="Ура-ура, новое упражнение!\n\n Давай попорядку: будет ли текст?")
    else:
        await callback.message.edit_text(text=text.admin_add_content_text)
    await callback.message.edit_reply_markup(reply_markup=get_admin_new_post_menu_kb())
    await callback.answer()


@router_admin.callback_query(F.data == skip_text_cd, AdminState.create_post)
async def skip_text(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    mes_to_delete = list((await state.get_data())[msg_delete])
    mes_to_delete.append(await callback.message.answer(text="Окей, тогда добавьте фото", reply_markup=return_kb()))

    await state.update_data(msg_delete=mes_to_delete)
    await state.set_state(AdminState.send_photo)


async def create_new_post_in_db(new_post_text: str, state: FSMContext):
    async for session in get_async_session():
        async with session.begin():
            prev_post_id = await session.execute(select(posts.c.id).order_by(posts.c.id.desc()))
            prev_post_id = prev_post_id.first()

            if prev_post_id: prev_post_id = prev_post_id[0]
            if new_post_text:
                result = await session.execute(
                    insert(posts).values(text=new_post_text, prev_post_id=prev_post_id,
                                         is_exercise=(await state.get_data())[is_ex],
                                         learning_section=SectionsId[(await state.get_data())[sections]].value))
            else:
                result = await session.execute(
                    insert(posts).values(prev_post_id=prev_post_id, is_exercise=(await state.get_data())[is_ex],
                                         learning_section=SectionsId[(await state.get_data())[sections]].value))

            await session.execute(update(users).where(users.c.next_post_id == None).values(
                next_post_id=result.inserted_primary_key[0]))

            await state.update_data(new_post_id=result.inserted_primary_key[0])
            if prev_post_id:
                await session.execute(
                    update(posts).where(posts.c.id == prev_post_id).values(
                        next_post_id=result.inserted_primary_key[0]))
            await session.commit()


async def delete_callback_list(del_list: list):
    for cl in del_list:
        await delete_callback(cl)


async def delete_callback(msg: Message):
    try:
        await msg.delete()
    except Exception:
        pass


@router_admin.message(AdminState.send_text, F.text)
async def admin_add_post_text(msg: Message, state: FSMContext):
    mes_to_delete = list((await state.get_data())[msg_delete])
    await delete_callback_list(mes_to_delete)
    await state.update_data(msg_delete={})
    mes_to_delete.clear()

    await create_new_post_in_db(msg.text, state)
    await delete_callback(msg)

    mes_to_delete.append(await msg.answer(text=msg.text))
    await state.update_data(msg_delete=mes_to_delete)

    if (await state.get_data())[is_ex]:
        p_text = f"Создано упражнение выше. Его id: {(await state.get_data())[new_post_id]}\nХотите добавить фото?"
    else:
        p_text = f"Создан пост выше. Его id: {(await state.get_data())[new_post_id]}\nХотите добавить фото?"

    await msg.answer(text=p_text, reply_markup=get_admin_add_photo_menu_kb())
    await state.set_state(AdminState.create_post)


@router_admin.message(F.media_group_id | F.photo, AdminState.send_text)
@media_group_handler
async def admin_add_post_text_incorrect(messages: List[Message], state: FSMContext):
    mes_to_delete = list((await state.get_data())[msg_delete])
    await delete_callback_list(mes_to_delete)
    await state.update_data(msg_delete={})
    mes_to_delete.clear()

    await delete_callback_list(messages)

    mes_to_delete.append(
        await messages[0].answer(text=f"Вы ошиблись и прислали не текст( \nПришлите текст", reply_markup=return_kb()))
    await state.update_data(msg_delete=mes_to_delete)


@router_admin.callback_query(F.data == add_photo_text_cd, AdminState.create_post)
async def add_post_photo(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.send_photo)
    mes_to_delete = list((await state.get_data())[msg_delete])
    await delete_callback_list(mes_to_delete)
    await state.update_data(msg_delete={})
    mes_to_delete.clear()

    mes_to_delete.append(await callback.message.edit_text(text="Пришлите фото", reply_markup=return_kb()))
    await state.update_data(msg_delete=mes_to_delete)
    await callback.answer()


@router_admin.message(AdminState.send_photo, lambda message: message.content_type != types.ContentType.PHOTO)
async def get_photo_incorrect(msg: Message, state: FSMContext):
    await state.set_state(AdminState.send_photo)
    mes_to_delete = list((await state.get_data())[msg_delete])
    await delete_callback_list(mes_to_delete)
    await state.update_data(msg_delete={})
    mes_to_delete.clear()

    await delete_callback(msg)
    mes_to_delete.append(
        await msg.answer(text=f"Вы ошиблись и прислали не фото(\n", reply_markup=return_kb()))
    await state.update_data(msg_delete=mes_to_delete)


@router_admin.message(F.media_group_id | F.photo, AdminState.send_photo)
@media_group_handler
async def album_handler(messages: List[Message], state: FSMContext):
    new_photos = [message.photo[-1].file_id for message in messages]

    if len((await state.get_data())) == 0 or (await state.get_data())[new_post_id] == {}:
        await create_new_post_in_db("", state)

    async for session in get_async_session():
        async with session.begin():
            for new_photo in new_photos:
                await session.execute(
                    insert(photos).values(file_id=new_photo, post_id=(await state.get_data())[new_post_id]))

            await session.execute(update(users).where(users.c.next_post_id is None).values(
                next_post_id=(await state.get_data())[new_post_id]))
            await session.commit()
    await delete_callback_list(messages)
    await end_create_post(messages[0], state)


async def end_create_post(msg: Message, state: FSMContext):
    await state.set_state(AdminState.send_photo)
    mes_to_delete = list((await state.get_data())[msg_delete])
    await delete_callback_list(mes_to_delete)
    await state.update_data(msg_delete={})
    mes_to_delete.clear()

    if len((await state.get_data())) != 0 and (await state.get_data())[new_post_id] != {}:
        await print_post((await state.get_data())[new_post_id], msg)

        if (await state.get_data())[is_ex]:
            p_text = f"Создано упражнение выше. Его id: {(await state.get_data())[new_post_id]}\n"
        else:
            p_text = f"Создан пост выше. Его id: {(await state.get_data())[new_post_id]}\n"
        await msg.answer(text=p_text)

    else:
        await msg.answer(text=f"Видимо поста не вышло..")

    await state.clear_data()
    await state.set_state(AdminState.admin_default)
    await msg.answer(text="Вот такое главное меню", reply_markup=main_menu.get_admin_main_menu_kb(
        await get_status(msg.chat.id)))


@router_admin.callback_query(F.data == return_cd, AdminState.send_photo)
async def return_to_choose_item(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.create_post)

    mes_to_delete = list((await state.get_data())[msg_delete])
    await delete_callback_list(mes_to_delete)
    await state.update_data(msg_delete={})
    mes_to_delete.clear()

    if len((await state.get_data())) == 0 or (await state.get_data())[new_post_id] == {}:
        await callback.message.answer(
            text=f"Вы выбрали категорию {SectionsNames[(await state.get_data())[sections][:-3]].value}\n\nДавай дальше: будет ли текст?",
            reply_markup=get_admin_new_post_menu_kb())
        await callback.answer()
    else:
        async for session in get_async_session():
            async with session.begin():
                text_p = await session.execute(
                    select(posts.c.text).where(posts.c.id == int((await state.get_data())[new_post_id])))
                await session.commit()
                text_p = text_p.first()[0]

        mes_to_delete.append(await callback.message.answer(text=text_p))
        await state.update_data(msg_delete=mes_to_delete)

        if (await state.get_data())[is_ex]:
            p_text = f"Создано упражнение выше. Его id: {(await state.get_data())[new_post_id]}\nХотите добавить фото?"
        else:
            p_text = f"Создан пост выше. Его id: {(await state.get_data())[new_post_id]}\nХотите добавить фото?"
        await callback.message.answer(text=p_text,
                                      reply_markup=get_admin_add_photo_menu_kb())
        await callback.answer()


@router_admin.callback_query(F.data == end_create_post_text_cd, AdminState.create_post)
async def admin_end_create(callback: types.CallbackQuery, state: FSMContext):
    await delete_callback(callback.message)
    await callback.answer()

    await end_create_post(callback.message, state)


@router_admin.message(AdminState.choose_section)
@router_admin.message(AdminState.create_post)
@media_group_handler
async def delete_incorrect_data(messages: List[Message]):
    await delete_callback_list(messages)
