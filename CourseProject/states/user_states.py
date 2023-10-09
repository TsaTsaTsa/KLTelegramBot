from aiogram.fsm.state import StatesGroup, State


class UserHello(StatesGroup):
    hello1 = State()
    hello2 = State()
    hello3 = State()
    main_info1 = State()
    main_info2 = State()


class UserState(StatesGroup):
    back_callback = State()
    forward_callback = State()
    forward_back_callback = State()
    done_callback = State()
    undone_callback = State()
    get_exercise = State()

    user_default = State()
