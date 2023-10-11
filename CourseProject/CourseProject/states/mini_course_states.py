from aiogram.fsm.state import StatesGroup, State


class Lesson(StatesGroup):
    first_lesson = State()
    second_lesson = State()
    third_lesson = State()
    fourth_lesson = State()
    fifth_lesson = State()
    sixth_lesson = State()
    end_course = State()


class Exercise(StatesGroup):
    first_exercise = State()
    second_exercise = State()
    third_exercise = State()
    fourth_exercise = State()
    fifth_exercise = State()
    sixth_exercise = State()


class IntroExercise(StatesGroup):
    intro1 = State()
    intro2 = State()
    intro3 = State()
    intro4 = State()
    intro5 = State()
