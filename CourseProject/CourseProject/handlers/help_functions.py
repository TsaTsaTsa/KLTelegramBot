from typing import Optional, Union

from aiogram import types
from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
from sqlalchemy import select, update, insert, delete

from database.database import get_async_session
from models.exercises_logs import exercise_logs
from models.photo import photos
from models.posts import posts
from models.posts_logs import post_logs
from models.users import users


async def print_post(print_post_id: int, msg: Message, reply_markup: Optional[
            Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]
        ] = None):
    async for session in get_async_session():
        async with session.begin():
            result_text = await session.execute(select(posts.c.text).where(posts.c.id == print_post_id))
            result_photo = await session.execute(select(photos.c.file_id).where(photos.c.post_id == print_post_id))
            await session.commit()

            result_photo = result_photo.fetchall()
            result_text = result_text.fetchone()
            callback_id = []

            if len(result_photo) == 1 and result_text and result_text[0]:
                callback_id.append(await msg.answer_photo(photo=result_photo[0][0], caption=result_text[0], reply_markup=reply_markup))
                return callback_id

            if result_photo:
                post_photo = ([types.InputMediaPhoto(media=photo_url[0]) for photo_url in
                               result_photo])
                callback_id.append(await msg.answer_media_group(media=post_photo))

            if result_text and result_text[0]:
                post_text = result_text[0]
                callback_id.append(await msg.answer(text=post_text, reply_markup=reply_markup))

            return callback_id


async def delete_post_by_id(delete_post_id: int):
    async for session in get_async_session():
        async with session.begin():
            post_to_delete = await session.execute(select(posts).where(posts.c.id == delete_post_id))
            post_to_delete = post_to_delete.all()
            prev_post_id = post_to_delete[0][3]
            next_post_id = post_to_delete[0][2]

            await session.execute(
                update(posts).where(posts.c.prev_post_id == delete_post_id).values(prev_post_id=prev_post_id))
            await session.execute(
                update(posts).where(posts.c.next_post_id == delete_post_id).values(next_post_id=next_post_id))
            await session.execute(
                update(users).where(users.c.next_post_id == delete_post_id).values(next_post_id=next_post_id))

            await session.execute(delete(photos).where(photos.c.post_id == delete_post_id))
            await session.execute(delete(post_logs).where(post_logs.c.post_id == delete_post_id))
            await session.execute(delete(exercise_logs).where(exercise_logs.c.exercise_id == delete_post_id))
            await session.execute(delete(posts).where(posts.c.id == delete_post_id))

            await session.commit()


async def create_user_db(user_id: int, user_status: str):
    async for session in get_async_session():
        async with session.begin():
            first_post_id = await session.execute(select(posts.c.id).order_by(posts.c.id))
            first_post_id = first_post_id.first()
            if first_post_id:
                first_post_id = first_post_id[0]

            await session.execute(insert(users).values(user_id=user_id, status=user_status, next_post_id=first_post_id))
            await session.commit()


async def get_status(us_id: int):
    async for session in get_async_session():
        async with session.begin():
            user_status = await session.execute(select(users.c.status).where(users.c.user_id == us_id))
            user_status = user_status.first()[0]
            await session.commit()

            return user_status
