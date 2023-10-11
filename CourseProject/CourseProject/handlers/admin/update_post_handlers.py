from typing import List

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_media_group import media_group_handler
from sqlalchemy import insert, select, update, delete
from aiogram import types

from database.database import get_async_session
from handlers.common import print_menu
from handlers.help_functions import print_post, delete_post_by_id
from kb.admin.callback import return_cd, \
    add_photo_text_cd, return_kb, choose_post_id_kb, \
    do_something_with_post_cd, choose_item_to_update_kb, \
    choose_text_to_update_text_cd, choose_photo_to_update_text_cd, choose_another_post_cd, end_update_text_cd, \
    continue_without_photo_cd, continue_with_out_text_kb, continue_without_text_text_cd, delete_or_update_post_kb, \
    return_to_item_menu_cd, get_update_photo_menu_kb
from kb.admin.main_menu import update_cd
from models.posts import posts
from models.photo import photos
from states.admin_states import AdminState

router_admin_update = Router()

update_p = 'update_p'
post_contain = [{'text': False}, {'photo': False}]
callback_to_delete = 'callback_to_delete'
print_post_id = 'print_post_id'


async def delete_callback_list(del_list: list):
    for cl in del_list:
        await delete_callback(cl)


async def delete_callback(msg: Message):
    try:
        await msg.delete()
    except Exception:
        pass


@router_admin_update.callback_query(F.data == update_cd, AdminState.admin_default)
async def get_id_to_update_post(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.get_post_id_update)
    await state.update_data(callback_to_delete={})
    await state.update_data(print_post_id={})

    callback_to_del = list((await state.get_data())[callback_to_delete])
    callback_to_del.append(await callback.message.edit_text(text="Введите id поста, который хотите обновить"))
    await state.update_data(callback_to_delete=callback_to_del)

    await callback.message.edit_reply_markup(reply_markup=return_kb())
    await callback.answer()


@router_admin_update.callback_query(F.data == return_cd, AdminState.updating_post)
@router_admin_update.callback_query(F.data == return_cd, AdminState.get_post_id_update)
async def return_to_main(callback: types.CallbackQuery, state: FSMContext):
    callback_to_del = list((await state.get_data())[callback_to_delete])
    await delete_callback_list(callback_to_del)
    print_post_to_delete_id = list((await state.get_data())[print_post_id])
    await delete_callback_list(print_post_to_delete_id)
    await state.update_data(print_post_id=[])
    await state.update_data(callback_to_delete=[])

    await state.set_state(AdminState.admin_default)

    await print_menu.print_main_menu_msg(callback.message, state)
    await callback.answer()


async def check_post_contain(state: FSMContext):
    async for session in get_async_session():
        async with session.begin():
            post_text = await session.execute(
                select(posts.c.text).where(posts.c.id == int((await state.get_data())[update_p])))
            post_photo = await session.execute(
                select(photos.c.file_id).where(photos.c.post_id == int((await state.get_data())[update_p])))
            await session.commit()

            post_text = post_text.fetchall()
            post_photo = post_photo.fetchall()
            post_contain[0]['text'] = len(post_text) != 0
            post_contain[1]['photo'] = len(post_photo) != 0


async def append_mes_to_del(callback_id: list, app_list: list):
    for cl in callback_id:
        if type(cl) is list:
            for cl1 in cl:
                app_list.append(cl1)
        else:
            app_list.append(cl)
    return app_list


@router_admin_update.message(AdminState.get_post_id_update, F.text)
async def choose_post_to_update(msg: types.Message, state: FSMContext):
    callback_to_dl = list((await state.get_data())[callback_to_delete])
    await delete_callback_list(callback_to_dl)
    await state.update_data(callback_to_delete=[])
    callback_to_dl = []
    try:
        await state.update_data(update_p=int(msg.text))
    except ValueError:
        callback_to_dl.append(msg)
        callback_to_dl.append(await msg.answer("Не похоже на число... Введите число", reply_markup=return_kb()))
        await state.update_data(callback_to_delete=callback_to_dl)
        return

    callback_id = await print_post((await state.get_data())[update_p], msg)
    if len(callback_id) == 0:
        callback_to_dl.append(msg)
        callback_to_dl.append(await msg.answer("Ооууу, такого поста нет. Скорее всего, вы ввели неверный id. "
                                               "\n\nВведите новый id", reply_markup=return_kb()))
        await state.update_data(callback_to_delete=callback_to_dl)
        await state.update_data(update_p=[])
    else:
        await msg.delete()
        await state.set_state(AdminState.updating_post)
        callback_to_dl = await append_mes_to_del(callback_id, callback_to_dl)

        callback_to_dl.append(
            await msg.answer(
                f"Вот пост c id: {(await state.get_data())[update_p]}\n\nХотите отредактировать этот пост?",
                reply_markup=choose_post_id_kb()))
        await state.update_data(callback_to_delete=callback_to_dl)
        await check_post_contain(state)


@router_admin_update.callback_query(F.data == choose_another_post_cd, AdminState.updating_post)
async def choose_another_post_to_update(callback: types.CallbackQuery, state: FSMContext):
    callback_to_del = list((await state.get_data())[callback_to_delete])
    await delete_callback_list(callback_to_del)
    print_post_to_delete_id = list((await state.get_data())[print_post_id])
    await delete_callback_list(print_post_to_delete_id)
    await state.update_data(print_post_id=[])
    await state.update_data(callback_to_delete=[])
    await state.update_data(update_p={})
    callback_to_del = []

    await state.set_state(AdminState.get_post_id_update)
    callback_to_del.append(
        await callback.message.answer(text="Введите id поста, который хотите обновить", reply_markup=return_kb()))
    await state.update_data(callback_to_delete=callback_to_del)
    await callback.answer()


@router_admin_update.message(lambda message: message.content_type != types.ContentType.TEXT,
                             AdminState.get_post_id_update)
@media_group_handler
async def choose_post_to_update_incorrect(messages: List[Message], state: FSMContext):
    callback_to_del = list((await state.get_data())[callback_to_delete])
    await delete_callback_list(callback_to_del)
    await state.update_data(callback_to_delete=[])
    callback_to_del = await append_mes_to_del(messages, callback_to_del)

    callback_to_del.append(
        await messages[0].answer(text=f"Вы ошиблись и прислали не id( \nПришлите id поста, который хотите изменить",
                                 reply_markup=return_kb()))
    await state.update_data(callback_to_delete=callback_to_del)


@router_admin_update.message(lambda message: message.content_type != types.ContentType.TEXT, AdminState.update_text)
@media_group_handler
async def update_text_incorrect_data(messages: List[Message], state: FSMContext):
    callback_to_del = list((await state.get_data())[callback_to_delete])
    await delete_callback_list(callback_to_del)
    await state.update_data(callback_to_delete=[])

    callback_to_del = await append_mes_to_del(messages, callback_to_del)
    callback_to_del.append(
        await messages[0].answer(text=f"Вы ошиблись и прислали не текст( \nПришлите текст поста",
                                 reply_markup=return_kb()))
    await state.update_data(callback_to_delete=callback_to_del)


@router_admin_update.callback_query(F.data == do_something_with_post_cd, AdminState.updating_post)
async def do_update_post(callback: types.CallbackQuery, state: FSMContext):
    callback_to_del = list((await state.get_data())[callback_to_delete])
    await delete_callback_list(callback_to_del)
    await state.update_data(callback_to_delete=[])
    callback_to_del = [await callback.message.answer("Выберите элемент", reply_markup=choose_item_to_update_kb())]
    await callback.answer()
    await state.update_data(callback_to_delete=callback_to_del)


@router_admin_update.callback_query(F.data == choose_text_to_update_text_cd, AdminState.updating_post)
async def choose_text_to_update(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.update_text)
    callback_to_del = list((await state.get_data())[callback_to_delete])
    await delete_callback_list(callback_to_del)
    await state.update_data(callback_to_delete=[])
    callback_to_del = [
        await callback.message.answer(text="Введите новый текст", reply_markup=continue_with_out_text_kb())]
    await state.update_data(callback_to_delete=callback_to_del)
    await callback.answer()


@router_admin_update.message(AdminState.update_text, F.text)
async def update_text(msg: Message, state: FSMContext):
    await delete_callback(msg)
    callback_to_del = list((await state.get_data())[callback_to_delete])
    await delete_callback_list(callback_to_del)
    print_post_to_delete_id = list((await state.get_data())[print_post_id])
    await delete_callback_list(print_post_to_delete_id)
    await state.update_data(print_post_id=[])
    await state.update_data(callback_to_delete=[])
    callback_to_del = []
    print_post_to_delete_id = []

    async for session in get_async_session():
        async with session.begin():
            await session.execute(
                update(posts).where(posts.c.id == int((await state.get_data())[update_p])).values(text=msg.text))
            await session.commit()

        await state.set_state(AdminState.updating_post)
        await append_mes_to_del(await print_post((await state.get_data())[update_p], msg), print_post_to_delete_id)
        callback_to_del.append(await msg.answer("Текст отредактирован\nХотите отредактировать что-то еще?",
                                                reply_markup=choose_item_to_update_kb()))
        await state.update_data(print_post_id=print_post_to_delete_id)
        await state.update_data(callback_to_delete=callback_to_del)


@router_admin_update.callback_query(F.data == choose_photo_to_update_text_cd, AdminState.updating_post)
async def choose_photo_to_update(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.update_photo)
    callback_to_del = list((await state.get_data())[callback_to_delete])
    await delete_callback_list(callback_to_del)

    callback_to_del = [
        await callback.message.answer(text="Выберите действие", reply_markup=get_update_photo_menu_kb())]
    await state.update_data(callback_to_delete=callback_to_del)
    await callback.answer()


@router_admin_update.callback_query(F.data == add_photo_text_cd, AdminState.update_photo)
async def get_photo(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.getting_photo)
    callback_to_del = list((await state.get_data())[callback_to_delete])
    await delete_callback_list(callback_to_del)

    callback_to_del = [await callback.message.answer(text="Пришлите новые фото", reply_markup=return_kb())]
    await state.update_data(callback_to_delete=callback_to_del)

    await callback.answer()


@router_admin_update.message(F.media_group_id | F.photo, AdminState.getting_photo)
@media_group_handler
async def album_handler(messages: List[Message], state: FSMContext):
    callback_to_del = list((await state.get_data())[callback_to_delete])
    await delete_callback_list(callback_to_del)
    print_post_to_delete_id = list((await state.get_data())[print_post_id])
    await delete_callback_list(print_post_to_delete_id)
    await state.update_data(print_post_id=[])
    await state.update_data(callback_to_delete=[])
    callback_to_del = []
    print_post_to_delete_id = []

    new_photos = [message.photo[-1].file_id for message in messages]
    await delete_callback_list(messages)

    async for session in get_async_session():
        await session.execute(delete(photos).where(photos.c.post_id == int((await state.get_data())[update_p])))
        for new_photo in new_photos:
            await session.execute(
                insert(photos).values(post_id=int((await state.get_data())[update_p]), file_id=new_photo))
        new_photos.clear()
        await session.commit()

    post_contain[1]['photo'] = True

    print_post_to_delete_id = await append_mes_to_del(await print_post((await state.get_data())[update_p], messages[0]),
                                                      print_post_to_delete_id)
    await state.set_state(AdminState.updating_post)
    callback_to_del.append(await messages[0].answer("Фото отредактировано\nХотите отредактировать что-то еще?",
                                                    reply_markup=choose_item_to_update_kb()))
    await state.update_data(print_post_id=print_post_to_delete_id)
    await state.update_data(callback_to_delete=callback_to_del)


@router_admin_update.callback_query(F.data == return_to_item_menu_cd, AdminState.update_text)
async def return_to_get_text(callback: types.CallbackQuery, state: FSMContext):
    print_post_to_delete_id = list((await state.get_data())[print_post_id])

    print_post_to_delete_id = await append_mes_to_del(
        await print_post((await state.get_data())[update_p], callback.message), print_post_to_delete_id)
    await choose_text_to_update(callback, state)

    await state.update_data(print_post_id=print_post_to_delete_id)


@router_admin_update.callback_query(F.data == return_to_item_menu_cd, AdminState.update_photo)
async def return_to_get_photo(callback: types.CallbackQuery, state: FSMContext):
    print_post_to_delete_id = list((await state.get_data())[print_post_id])

    print_post_to_delete_id = await append_mes_to_del(
        await print_post((await state.get_data())[update_p], callback.message), print_post_to_delete_id)
    await choose_photo_to_update(callback, state)
    await state.update_data(print_post_id=print_post_to_delete_id)


@router_admin_update.callback_query(F.data == return_cd, AdminState.update_text)
@router_admin_update.callback_query(F.data == return_cd, AdminState.update_photo)
async def return_to_choose_item_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.updating_post)
    await do_update_post(callback, state)


@router_admin_update.callback_query(F.data == end_update_text_cd, AdminState.updating_post)
async def end_update_post(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.admin_default)
    callback_to_del = list((await state.get_data())[callback_to_delete])
    await delete_callback_list(callback_to_del)
    print_post_to_delete_id = list((await state.get_data())[print_post_id])
    await delete_callback_list(print_post_to_delete_id)
    await state.update_data(print_post_id=[])
    await state.update_data(callback_to_delete=[])

    await print_post((await state.get_data())[update_p], callback.message)
    await callback.message.answer(f"Отредактирован пост с id: {(await state.get_data())[update_p]}")
    await callback.answer()

    await state.clear_data()
    await print_menu.print_main_menu_msg(callback.message, state)


@router_admin_update.callback_query(F.data == do_something_with_post_cd, AdminState.update_photo)
@router_admin_update.callback_query(F.data == do_something_with_post_cd, AdminState.update_text)
async def delete_post(callback: types.CallbackQuery, state: FSMContext):
    await delete_post_by_id((await state.get_data())[update_p])
    callback_to_del = list((await state.get_data())[callback_to_delete])
    await delete_callback_list(callback_to_del)

    await state.set_state(AdminState.admin_default)
    await callback.message.answer(f"Пост c id: {(await state.get_data())[update_p]} удален")
    await state.update_data(update_p={})
    await state.clear_data()

    await print_menu.print_main_menu_msg(callback.message, state)


@router_admin_update.callback_query(F.data == continue_without_photo_cd, AdminState.update_photo)
async def delete_photo_post(callback: types.CallbackQuery, state: FSMContext):
    callback_to_del = list((await state.get_data())[callback_to_delete])
    await delete_callback_list(callback_to_del)
    print_post_to_delete_id = list((await state.get_data())[print_post_id])
    await delete_callback_list(print_post_to_delete_id)
    await state.update_data(print_post_id=[])
    await state.update_data(callback_to_delete=[])
    callback_to_del.clear()
    print_post_to_delete_id.clear()

    if not post_contain[0]['text'] and post_contain[1]['photo']:
        callback_to_del.append(
            await callback.message.answer("Хотите удалить пост?", reply_markup=delete_or_update_post_kb()))
        await callback.answer()
        await state.update_data(callback_to_delete=callback_to_del)
        return

    async for session in get_async_session():
        await session.execute(delete(photos).where(photos.c.post_id == int((await state.get_data())[update_p])))
        await session.commit()

    post_contain[1]['photo'] = False
    print_post_to_delete_id = await append_mes_to_del(
        await print_post((await state.get_data())[update_p], callback.message), print_post_to_delete_id)
    await state.set_state(AdminState.updating_post)

    callback_to_del.append(await callback.message.answer("Фото отредактировано\nХотите отредактировать что-то еще?",
                                                         reply_markup=choose_item_to_update_kb()))
    await callback.answer()
    await state.update_data(print_post_id=print_post_to_delete_id)
    await state.update_data(callback_to_delete=callback_to_del)


@router_admin_update.callback_query(F.data == continue_without_text_text_cd, AdminState.update_text)
async def delete_text_update(callback: types.CallbackQuery, state: FSMContext):
    callback_to_del = list((await state.get_data())[callback_to_delete])
    await delete_callback_list(callback_to_del)
    print_post_to_delete_id = list((await state.get_data())[print_post_id])
    await delete_callback_list(print_post_to_delete_id)
    await state.update_data(print_post_id=[])
    await state.update_data(callback_to_delete=[])
    callback_to_del.clear()
    print_post_to_delete_id.clear()

    if post_contain[0]['text'] and not post_contain[1]['photo']:
        callback_to_del.append(
            await callback.message.answer(text="Хотите удалить пост?", reply_markup=delete_or_update_post_kb()))
        await callback.answer()
        await state.update_data(callback_to_delete=callback_to_del)

        return

    async for session in get_async_session():
        async with session.begin():
            await session.execute(
                update(posts).where(posts.c.id == int((await state.get_data())[update_p])).values(text=None))
            await session.commit()

    post_contain[0]['text'] = False

    print_post_to_delete_id = await append_mes_to_del(
        await print_post((await state.get_data())[update_p], callback.message), print_post_to_delete_id)
    await state.set_state(AdminState.updating_post)

    callback_to_del.append(await callback.message.answer("Текст удален\nХотите отредактировать что-то еще?",
                                                         reply_markup=choose_item_to_update_kb()))
    await state.update_data(print_post_id=print_post_to_delete_id)
    await state.update_data(callback_to_delete=callback_to_del)


@router_admin_update.message(AdminState.update_post)
@router_admin_update.message(AdminState.updating_post)
@router_admin_update.message(AdminState.admin_default)
@media_group_handler
async def delete_incorrect_data(messages: List[Message]):
    await delete_callback_list(messages)
