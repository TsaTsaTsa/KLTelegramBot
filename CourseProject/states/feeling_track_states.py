from aiogram.fsm.state import StatesGroup, State


class FeelingHelpStates(StatesGroup):
    help1 = State()
    help2 = State()
    help3 = State()
    get_skip = State()


class TrackerStates(StatesGroup):
    choose_feeling = State()
    get_user_text_feeling = State()
    got_user_text_feeling = State()
    get_describe_text = State()
    got_describe_text = State()


class OnOffStates(StatesGroup):
    to_on_state = State()
    to_off_state = State()
    got_user_text_feeling = State()
    get_describe_text = State()
    got_describe_text = State()
