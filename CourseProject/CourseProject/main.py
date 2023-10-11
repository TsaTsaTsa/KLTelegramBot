import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select, update, insert

from core import config
from database.database import get_async_session
from handlers.admin.hello import router_ah
from handlers.admin.create_post import router_admin
from handlers.admin.delete_post_handlers import router_admin_delete
from handlers.admin.on_off_bot_admin import on_off_bot_admin_router
from handlers.admin.update_post_handlers import router_admin_update
from handlers.common.hello import router_h
from handlers.common.mini_course import router_mini_course
from handlers.common.print_menu import router_mm
from handlers.common.statistic import router_statistic
from handlers.feeling_tracker.help_tracker import router_ht
from handlers.common.exercise_handelrs import exercise_router
from handlers.feeling_tracker.on_off_tracker_handlers import on_off_tracker_router
from handlers.users.hello import router_uh
from handlers.common.tracker_handlers import tracker_router
from handlers.users.on_off_bot_user import on_off_bot_user_router
from kb.exrcises_cb.exercises_callback import exercise_undone_kb
from kb.feeling_tracker.getting_feelings_kb import mood_tracker_main_menu
from models.exercises_logs import exercise_logs
from models.feeling_logs import feeling_logs
from models.photo import photos
from models.posts import posts
from models.posts_logs import post_logs
from models.users import users, Status
from res.media_files.media_files_id import url_after_course

bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)


async def send_post():
    async for session in get_async_session():
        async with session.begin():
            users_post_id = await session.execute(
                select(users.c.user_id, users.c.next_post_id).where(users.c.status != Status.coursing.name,
                                                                    users.c.status != Status.inactive.name))
            users_post_id = users_post_id.fetchall()

            for user_id, post_id in users_post_id:
                if post_id is None: continue
                cur_post = await session.execute(
                    select(posts.c.text, posts.c.is_exercise, posts.c.learning_section).where(posts.c.id == int(post_id)))
                cur_post = cur_post.fetchall()
                post_text = cur_post[0][0]
                is_exercise = cur_post[0][1]

                post_photos = await session.execute(select(photos.c.file_id).where(photos.c.post_id == int(post_id)))
                post_photos = post_photos.fetchall()

                if is_exercise:

                    await session.execute(
                        insert(exercise_logs).values(user_id=user_id, exercise_id=post_id,
                                                     date_get_exercise=datetime.today(), is_done=False,
                                                     is_done_last_month=False,
                                                     section_id=cur_post[0][2]))
                else:
                    await session.execute(
                        insert(post_logs).values(user_id=user_id, post_id=post_id,
                                                     date_get_post=datetime.today(),
                                                     section_id=cur_post[0][2]))

                post_photos = [types.InputMediaPhoto(media=post[0]) for post in post_photos]
                if post_photos:
                    await bot.send_media_group(user_id, media=post_photos)
                if post_text:
                    if is_exercise:
                        await bot.send_message(user_id, text=post_text, reply_markup=exercise_undone_kb())
                    else:
                        await bot.send_message(user_id, text=post_text)

                next_post_id = await session.execute(select(posts.c.next_post_id).where(posts.c.id == int(post_id)))
                next_post_id = next_post_id.first()[0]
                await session.execute(
                    update(users).where(users.c.user_id == int(user_id)).values(next_post_id=next_post_id))
                await session.commit()


async def send_tracker():
    async for session in get_async_session():
        async with session.begin():
            users_active_track = await session.execute(
                select(users.c.user_id).where(users.c.status == Status.on_feeling_tracker.name))
            users_active_track = users_active_track.fetchall()
            await session.commit()

            for user_id in users_active_track:
                await bot.send_photo(int(user_id[0]), photo=url_after_course[2],
                                     caption="Привет, это твой трекер)\nСамое время тренировать свои чувства!"
                                             "\n\nПожалуйста, выбери один из вариантов ниже",
                                     reply_markup=mood_tracker_main_menu())


async def get_text(user_logs):
    text = ""
    if len(user_logs) == 0:
        return "\nНичего не отметил("
    for log in user_logs:
        text+=f"\n<b>{log[0].day}.{log[0].month}.{log[0].year}</b> Ты чувствовал: {log[1]}\n"
        if log[2] is not None:
            text+=f"Ты дополнял: {log[2]}"
    text+= "\n\nОбнимаем)"
    return text


async def send_tracker_statistic():
    async for session in get_async_session():
        async with session.begin():
            users_active_track = await session.execute(
                select(users.c.user_id, users.c.id).where(users.c.status == Status.on_feeling_tracker.name))
            users_active_track = users_active_track.fetchall()

            r = (datetime.today() - timedelta(days=7))
            for user_id in users_active_track:
                user_logs = await session.execute(
                    select(feeling_logs.c.date, feeling_logs.c.feeling_str, feeling_logs.c.describe).
                    where(feeling_logs.c.user_id == int(user_id[1])).where(feeling_logs.c.date >= r))
                user_logs = user_logs.fetchall()
                text = "Привет, это твой трекер)\nВремя подводить итоги!)\n\n"\
                       "На этой неделе\n" + await get_text(user_logs)

                await bot.send_message(int(user_id[0]), text=text)
            await session.commit()


async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(router_h, router_mm, router_ah, router_mini_course, router_ht, router_uh, router_admin_update,
                       router_admin, router_admin_delete, tracker_router,
                       exercise_router, on_off_tracker_router, router_statistic, on_off_bot_admin_router,
                       on_off_bot_user_router)
    scheduler = AsyncIOScheduler()

    # scheduler.add_job(send_post, trigger="cron", day_of_week='mon,fri', hour=5, minute=30)
    # scheduler.add_job(send_tracker_statistic, trigger="cron", day_of_week='sun', hour=12, minute=0)
    # scheduler.add_job(send_tracker,  trigger="cron", day_of_week='mon-sun', hour=12, minute=0)
    scheduler.add_job(send_post,  trigger="interval", seconds=5)
    # scheduler.add_job(send_tracker_statistic,  trigger="cron", day=10, month=10, year=2023, hour=23, minute=40)

    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
