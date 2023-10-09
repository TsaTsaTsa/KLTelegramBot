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
                       func.count().filter(exercise_logs.c.is_done == True),
                       func.count(),
                       func.count().filter(exercise_logs.c.date_change_status >= cur_month_filter).
                       filter(exercise_logs.c.is_done == True),
                       func.count().filter(exercise_logs.c.date_change_status >= last_month_filter).filter(
                           cur_month_filter > exercise_logs.c.date_get_exercise).
                       filter(exercise_logs.c.is_done_last_month == True),
                       func.count().filter(exercise_logs.c.date_get_exercise >= cur_month_filter).filter(
                           exercise_logs.c.is_done == True),
                       func.count().filter(exercise_logs.c.date_get_exercise >= cur_month_filter)
                       ).group_by(exercise_logs.c.user_id))
            count_don_exercise = count_don_exercise.fetchall()
            user_ = [u for u in count_don_exercise if u and u[0] == chat_id]
            if len(user_) == 0:
                return None

            user_ = user_[0]
            count_exercise_done_all_time, count_exercise_all_time = user_[2], user_[3]
            cof_efficiency = count_exercise_done_all_time / count_exercise_all_time

            count_exercise_all_time_more = 0 if (len(count_don_exercise) - 1) == 0 else len(
                [c for c in count_don_exercise if c[2] / c[3] < cof_efficiency]) / (len(count_don_exercise) - 1) * 100

            perc_done_get_this_month = 0 if user_[7] == 0 else user_[6] / user_[7] * 100

            count_perc_done_get_this_month_more = 0 if (len(count_don_exercise) - 1) == 0 else len(
                [c for c in count_don_exercise if c[6] < perc_done_get_this_month]) / (len(count_don_exercise) - 1) * 100

            return [(datetime.today() - user_[1]).days + 1, user_[2], user_[3], count_exercise_all_time_more, user_[4],
                    user_[5], perc_done_get_this_month, count_perc_done_get_this_month_more]


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

    statistic_text = f'<b>Статистика!)</b>\n\nВы занимаетесь уже {info[0]} {await get_word(info[0], "день", "дня", "дней")}\n\n' \
                     f'<b>За это время</b> мы прислали вам {info[2]} {await get_word(info[1], "упражнение", "упражнения", "упражнений")}. Сейчас из них выполнены {info[1]}. \n' \
                     f'Это больше чем у {round(info[3])}% других пользователей.\n\n' \
                     f'<b>В этом месяце</b> вы выполнили {info[4]} {await get_word(info[4], "упражнение", "упражнения", "упражнений")}' \
                     f'. Это на {abs(info[4] - info[5])} {await get_word(abs(info[4] - info[5]), "упражнение", "упражнения", "упражнений")}' \
                     f' {"больше" if info[4] - info[5] > 0 else "меньше"}, чем в прошлом месяце.\n\n' \
                     f'Вы уже выполнили {round(info[6])}% <b>присланных в этом месяце упражнений</b>. \nЭто столько же/больше чем у {100}% пользователей\n\nВы молодец!)'
    return statistic_text
