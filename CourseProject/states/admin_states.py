from aiogram.fsm.state import StatesGroup, State


class AdminHelpStates(StatesGroup):
    help1 = State()
    help2 = State()
    help3 = State()


class AdminState(StatesGroup):
    admin_default = State()
    create_post = State()
    create_exercise = State()
    get_post_id_update = State()
    update_post = State()
    update_text = State()
    delete_photo = State()
    update_photo = State()
    end_update = State()
    redy_update = State()
    activate_feeling_track = State()
    inactivate_feeling_track = State()
    delete_post = State()
    choose_post_to_del = State()
    updating_post = State()
    getting_photo = State()

    send_text = State()
    send_photo = State()

    restart_first_lesson = State()
    restart_second_lesson = State()
    restart_third_lesson = State()
    restart_fourth_lesson = State()
    restart_fifth_lesson = State()
    restart_sixth_lesson = State()
    restart_end_course = State()
