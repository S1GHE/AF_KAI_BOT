from aiogram.dispatcher.filters.state import StatesGroup, State


class register(StatesGroup):
    """
    Ветка регистрации
    """
    user_id = State()
    user_status = State()
    user_name = State()
    user_last_name = State()
    user_numbers_groups = State()
    user_mailing = State()
    user_answer = State()


class lessons(StatesGroup):
    """
    Ветка расписания
    """
    user_answer_les_start = State()
    user_answer_your_les = State()
    user_answer_number_les = State()
    user_answer_number_les2 = State()


class report(StatesGroup):
    user_report = State()
