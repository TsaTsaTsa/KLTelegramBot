from typing import List

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_media_group import media_group_handler

from handlers.common import print_menu
from handlers.help_functions import print_post, delete_post_by_id
from kb.admin.callback import return_kb, choose_post_id_kb, choose_another_post_cd, \
    return_cd, do_something_with_post_cd
from kb.admin.main_menu import delete_post_cd
from states.admin_states import AdminState

router_admin_delete = Router()

delete_p = 'delete_p'
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


async def append_mes_to_del(callback_id: list, app_list: list):
    for cl in callback_id:
        if type(cl) is list:
            for cl1 in cl:
                app_list.append(cl1)
        else:
            app_list.append(cl)
    return app_list


@router_admin_delete.callback_query(F.data == do_something_with_post_cd, AdminState.choose_post_to_del)
async def delete_post(callback: types.CallbackQuery, state: FSMContext):
    callback_to_del = list((await state.get_data())[callback_to_delete])
    await delete_callback_list(callback_to_del)
    print_post_to_delete_id = list((await state.get_data())[print_post_id])
    await delete_callback_list(print_post_to_delete_id)
    await state.update_data(print_post_id={})
    await state.update_data(callback_to_delete={})

    await delete_post_by_id((await state.get_data())[delete_p])

    await state.set_state(AdminState.admin_default)
    await callback.message.answer(f"Пост c id: {(await state.get_data())[delete_p]} удален")

    await state.clear_data()
    await print_menu.print_main_menu_msg(callback.message, state)


@router_admin_delete.callback_query(F.data == delete_post_cd, AdminState.admin_default)
@router_admin_delete.callback_query(F.data == choose_another_post_cd, AdminState.choose_post_to_del)
async def choose_post_to_delete(callback: types.CallbackQuery, state: FSMContext):
    if await state.get_state() == AdminState.choose_post_to_del:
        print_post_to_delete_id = list((await state.get_data())[print_post_id])
        await delete_callback_list(print_post_to_delete_id)
        
    await state.update_data(print_post_id={})
    await state.update_data(delete_p={})
    await state.update_data(callback_to_delete={})

    await state.set_state(AdminState.delete_post)
    callback_to_del = list((await state.get_data())[callback_to_delete])
    callback_to_del.append(await callback.message.edit_text(text="Введите id поста, который хотите удалить"))
    await state.update_data(callback_to_delete=callback_to_del)

    await callback.message.edit_reply_markup(reply_markup=return_kb())
    await callback.answer()


@router_admin_delete.message(AdminState.delete_post, F.text)
async def choose_post_to_delete(msg: types.Message, state: FSMContext):
    callback_to_del = list((await state.get_data())[callback_to_delete])
    await delete_callback_list(callback_to_del)
    callback_to_del = []
    await state.update_data(callback_to_delete={})

    try:
        await state.update_data(delete_p=int(msg.text))
    except ValueError:
        callback_to_del.append(msg)
        callback_to_del.append(await msg.answer("Не похоже на число... Введите число", reply_markup=return_kb()))
        await state.update_data(callback_to_delete=callback_to_del)
        await state.update_data(delete_p={})
        return

    callback_id = await print_post((await state.get_data())[delete_p], msg)
    if len(callback_id) == 0:
        callback_to_del.append(msg)
        callback_to_del.append(await msg.answer("Ооууу, такого поста нет. Скорее всего, вы ввели неверный id. "
                                                "Введите новый id", reply_markup=return_kb()))

        await state.update_data(callback_to_delete=callback_to_del)
        await state.update_data(delete_p={})
    else:
        await delete_callback(msg)

        await state.set_state(AdminState.choose_post_to_del)
        callback_to_del.append(
            await msg.answer(f"Пост с id: {(await state.get_data())[delete_p]}\nХотите удалить этот пост?",
                             reply_markup=choose_post_id_kb()))
        print_post_to_delete_id = list((await state.get_data())[print_post_id])
        print_post_to_delete_id = await append_mes_to_del(callback_id, print_post_to_delete_id)
        await state.update_data(print_post_id=print_post_to_delete_id)
        await state.update_data(callback_to_delete=callback_to_del)


@router_admin_delete.callback_query(F.data == return_cd, AdminState.choose_post_to_del)
@router_admin_delete.callback_query(F.data == return_cd, AdminState.delete_post)
async def return_to_choose_item(callback: types.CallbackQuery, state: FSMContext):
    callback_to_del = list((await state.get_data())[callback_to_delete])
    await delete_callback_list(callback_to_del)
    print_post_to_delete_id = list((await state.get_data())[print_post_id])
    await delete_callback_list(print_post_to_delete_id)

    await state.update_data(print_post_id={})
    await state.update_data(callback_to_delete={})
    await state.update_data(delete_p={})

    await state.set_state(AdminState.admin_default)
    await print_menu.print_main_menu_msg(callback.message, state)


@router_admin_delete.message(lambda message: message.content_type != types.ContentType.TEXT, AdminState.delete_post)
@media_group_handler
async def choose_post_to_update_incorrect(messages: List[Message], state:FSMContext):
    callback_to_del = list((await state.get_data())[callback_to_delete])
    await delete_callback_list(callback_to_del)
    await state.update_data(callback_to_delete={})

    callback_to_del = await append_mes_to_del(messages, callback_to_del)
    callback_to_del.append(
        await messages[0].answer(text=f"Вы ошиблись и прислали не id( \nПришлите id поста, который хотите удалить",
                                 reply_markup=return_kb()))
    await state.update_data(callback_to_delete=callback_to_del)


@router_admin_delete.message(AdminState.choose_post_to_del)
@media_group_handler
async def delete_incorrect_data(messages: List[Message]):
    await delete_callback_list(messages)
