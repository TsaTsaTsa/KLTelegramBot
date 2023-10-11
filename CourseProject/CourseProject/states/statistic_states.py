from aiogram.fsm.state import StatesGroup, State


class StatisticState(StatesGroup):
    get_statistic = State()
