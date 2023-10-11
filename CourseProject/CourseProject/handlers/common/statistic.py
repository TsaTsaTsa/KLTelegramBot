from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy import select, func

from database.database import get_async_session
from handlers.common import print_menu
from kb.admin.main_menu import statistics_cd
from kb.admin.statistic_callback import close_statistic_kb, close_cd
from models.exercises_logs import exercise_logs
from models.posts_logs import post_logs
from states.admin_states import AdminState
from states.statistic_states import StatisticState
from states.user_states import UserState

cur_month_filter = datetime(day=1, month=datetime.today().month, year=datetime.today().year)
last_month_filter = datetime(day=1, month=12 if datetime.today().month - 1 == 0 else datetime.today().month - 1,
                             year=datetime.today().year)

router_statistic = Router()


async def get_statistic(chat_id: int):
    async for session in get_async_session():
        async with session.begin():
            count_don_exercise = await session.execute(
                select(exercise_logs.c.user_id,
                       func.min(exercise_logs.c.date_get_exercise),
                       func.count().filter(exercise_logs.c.is_done == True).filter(exercise_logs.c.section_id == 1),
                       func.count().filter(exercise_logs.c.section_id == 1),
                       func.count().filter(exercise_logs.c.is_done == True).filter(exercise_logs.c.section_id == 2),
                       func.count().filter(exercise_logs.c.section_id == 2),
                       func.count().filter(exercise_logs.c.is_done == True).filter(exercise_logs.c.section_id == 3),
                       func.count().filter(exercise_logs.c.section_id == 3),
                       func.count().filter(exercise_logs.c.is_done == True).filter(exercise_logs.c.section_id == 4),
                       func.count().filter(exercise_logs.c.section_id == 4),
                       func.count().filter(exercise_logs.c.is_done == True).filter(exercise_logs.c.section_id == 5),
                       func.count().filter(exercise_logs.c.section_id == 5),
                       func.count().filter(exercise_logs.c.is_done == True).filter(exercise_logs.c.section_id == 6),
                       func.count().filter(exercise_logs.c.section_id == 6),
                       func.count().filter(exercise_logs.c.is_done == True).filter(exercise_logs.c.section_id == 7),
                       func.count().filter(exercise_logs.c.section_id == 7),
                       func.count().filter(exercise_logs.c.is_done == True),
                       func.count().filter(),
                       func.count().filter(exercise_logs.c.date_change_status >= cur_month_filter).filter(exercise_logs.c.is_done == True),
                       func.count().filter(exercise_logs.c.is_done_last_month)
                       + func.count().filter(exercise_logs.c.date_change_status >= last_month_filter).filter(exercise_logs.c.is_done == True).filter(exercise_logs.c.date_change_status < cur_month_filter)
                       ).group_by(exercise_logs.c.user_id))
            count_had_post = await session.execute(select(
                post_logs.c.user_id,
                func.count().filter(post_logs.c.user_id == chat_id).filter(post_logs.c.section_id == 1),
                func.count().filter(post_logs.c.user_id == chat_id).filter(post_logs.c.section_id == 2),
                func.count().filter(post_logs.c.user_id == chat_id).filter(post_logs.c.section_id == 3),
                func.count().filter(post_logs.c.user_id == chat_id).filter(post_logs.c.section_id == 4),
                func.count().filter(post_logs.c.user_id == chat_id).filter(post_logs.c.section_id == 5),
                func.count().filter(post_logs.c.user_id == chat_id).filter(post_logs.c.section_id == 6),
                func.count().filter(post_logs.c.user_id == chat_id).filter(post_logs.c.section_id == 7)
            ).where(post_logs.c.user_id == chat_id).group_by(post_logs.c.user_id))
            count_had_post = count_had_post.fetchall()

            await session.commit()
            count_don_exercise = count_don_exercise.fetchall()
            user_ = [u for u in count_don_exercise if u and u[0] == chat_id]
            if len(user_) == 0 or len(count_had_post) == 0:
                return None

            user_ = user_[0]
            count_exercises_by_method = user_[2:16]
            perc_material_is_done = 0 if user_[17] == 0 else user_[16] / user_[17]
            t = []
            for c in count_don_exercise:
                if c[0] != user_ and (0 if c[17] == 0 else c[16] / c[17] < perc_material_is_done):
                    t.append(c)
            perc_more_than_users = 0 if len(count_don_exercise) - 1 == 0 else len(t) / (len(count_don_exercise) - 1)
            count_done_this_month = user_[18]
            count_done_last_month = user_[19]
            return [(datetime.today() - user_[1]).days + 1, list(count_had_post[0][1:]), list(count_exercises_by_method),
                    round(perc_material_is_done * 100),
                    round(perc_more_than_users * 100), count_done_this_month, count_done_this_month - count_done_last_month]


@router_statistic.callback_query(F.data == statistics_cd, UserState.user_default)
@router_statistic.callback_query(F.data == statistics_cd, AdminState.admin_default)
async def print_statistic(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StatisticState.get_statistic)

    await callback.message.delete()
    await callback.message.answer(text=await get_statistic_text(await get_statistic(callback.message.chat.id)),
                                  reply_markup=close_statistic_kb())
    await callback.answer()


@router_statistic.callback_query(F.data == close_cd, StatisticState.get_statistic)
async def close_statistic(callback: CallbackQuery, state: FSMContext):
    await print_menu.print_main_menu_msg(callback.message, state)


async def get_word(info: int, word_1, word_2, word_3):
    return word_1 if info == 1 else word_2 if 2 <= info <= 4 else word_3


async def get_statistic_text(info: list):
    if info is None:
        return "Статистика пока не получится(\nМы слишком мало знаем друг-друга"

    statistic_text = f"<b>Мы вместе</b> уже уже дней {info[0]} дней\n\nЗа это время вы изучили:\n" \
                     f"<b>{info[1][0]}</b> {await get_word(info[1][0], 'пост', 'поста', 'постов')} <b>по методу Демидова\n</b>" \
                     f"<b>{info[1][1]}</b> {await get_word(info[1][1], 'пост', 'поста', 'постов')} <b>по методу Кнебель\n</b>" \
                     f"<b>{info[1][2]}</b> {await get_word(info[1][2], 'пост', 'поста', 'постов')} <b>по методу Чехова\n</b>" \
                     f"<b>{info[1][3]}</b> {await get_word(info[1][3], 'пост', 'поста', 'постов')} <b>по методу Станиславского</b>\n" \
                     f"<b>{info[1][4]}</b> {await get_word(info[1][4], 'пост', 'поста', 'постов')} <b>по медитациям</b>\n" \
                     f"<b>{info[1][5]}</b> {await get_word(info[1][5], 'пост', 'поста', 'постов')} <b>по качества</b>\n" \
                     f"<b>{info[1][6]}</b> {await get_word(info[1][6], 'пост', 'поста', 'постов')} <b>по другим темам)</b>\n\n" \
                     f"За это время вы выполнили:\n" \
                     f"<b>{info[2][0]}</b> из {info[2][1]} {await get_word(info[2][1], 'упражнение', 'упражнения', 'упражнений')} <b>по методу Демидова\n</b>" \
                     f"<b>{info[2][2]}</b> из {info[2][3]} {await get_word(info[2][3], 'упражнение', 'упражнения', 'упражнений')} <b>по методу Кнебель\n</b>" \
                     f"<b>{info[2][4]}</b> из {info[2][5]} {await get_word(info[2][5], 'упражнение', 'упражнения', 'упражнений')} <b>по методу Чехова\n</b>" \
                     f"<b>{info[2][6]}</b> из {info[2][7]} {await get_word(info[2][7], 'упражнение', 'упражнения', 'упражнений')} <b>по методу Станиславского\n</b>" \
                     f"<b>{info[2][8]}</b> из {info[2][9]} {await get_word(info[2][9], 'упражнение', 'упражнения', 'упражнений')} <b>по медитациям\n</b>" \
                     f"<b>{info[2][10]}</b> из {info[2][11]} {await get_word(info[2][11], 'упражнение', 'упражнения', 'упражнений')} <b>качества\n</b>" \
                     f"<b>{info[2][12]}</b> из {info[2][13]} {await get_word(info[2][13], 'упражнение', 'упражнения', 'упражнений')} <b>по другим темам\n\n</b>" \
                     f"Всего вы изучили <b>{info[3]}%</b> полученного материала!)\nЭто больше, чем у <b>{info[4]}%</b> пользователей.\n\n" \
                     f"В этом месяце вы выполнили <b>{info[5]}</b> упражнений.\nЭто на <b>{abs(info[6])}</b> <b>{'больше' if info[6] >= 0 else 'меньше'}</b>, чем в прошлом месяце.\n\n" \
                     f"Ты молодец!"
    return statistic_text
