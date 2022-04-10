import KeyBoard
from Lib import Data_work
from LocalDataLessons import Lessons
from main import bot, dp
from Config import config
from Data import DataBase
from KeyBoard import status_menu, confirmation_menu
from Loader import register, lessons, report
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext


async def get_default_commands(dp):
    await bot.set_my_commands(
        [
            types.BotCommand("start", "Начало работы"),
            types.BotCommand("reg", "Регистрация"),
            types.BotCommand("les", "Расписание"),
            types.BotCommand("report", "Сообщить об ошибке"),
            types.BotCommand("week", "Четность/Нечетность недели")
        ]
    )
    await bot.send_message(chat_id=config.admin_id, text="Бот запущен")


# Todo ---------------------------------------- Start -----------------------------------------------------------------
@dp.message_handler(Command("start"))
async def start(message: types.Message):
    await message.answer(f"Привет {message.from_user.first_name} 😉\n\n"
                         f"<b>Телеграмма от разработчиков</b>\n"
                         f"Бот находится в стадии разработки, и мы были бы рады,"
                         f" если именно ты помог нам в тестировании! "
                         f"Тестирование будет закончено через неделю\n\n"
                         f"<b>Для начала работы с ботом, тебе следует зарегистрироваться</b>: /reg",
                         parse_mode=types.ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())


# Todo -------------------------------------- Register Branch ---------------------------------------------------------
@dp.message_handler(Command("reg"))
async def register_step_start(message: types.Message):
    if DataBase.get_availability_user(message.from_user.id) == 1:
        await message.answer("<b>Вы начали регистрацию</b>\n\n"
                             "Для начала, нам надо узнать кто вы",
                             parse_mode=types.ParseMode.HTML, reply_markup=status_menu)
        await register.user_status.set()
    else:
        await message.answer("Упс... 😕\n"
                             "Ваш аккаунт уже зарегистрирован")


@dp.message_handler(state=register.user_status)
async def register_step_status(message: types.Message, state: FSMContext):
    if message.text == "Я студент 👨‍🎓":
        await state.update_data(user_id=message.from_user.id, user_status="Студент")
    elif message.text == "Я преподаватель 👨‍🏫":
        await state.update_data(user_id=message.from_user.id, user_status="Преподаватель")
    else:
        await message.answer("Пользуйтесь кнопками для ответа")
        return
    await message.answer("Введите свое имя", reply_markup=types.ReplyKeyboardRemove())
    await register.user_name.set()


@dp.message_handler(state=register.user_name)
async def register_step_name(message: types.Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await message.answer("Введите свою фамилию")
    await register.user_last_name.set()


@dp.message_handler(state=register.user_last_name)
async def register_step_last_name(message: types.Message, state: FSMContext):
    await state.update_data(user_last_name=message.text)
    user_info = await state.get_data()
    if user_info["user_status"] == "Студент":
        await message.answer("Введите номер своей академической группы")
        await register.user_numbers_groups.set()
    else:
        await state.update_data(user_numbers_groups="None")
        await message.answer(f"Ваша должность: {user_info['user_status']}\n"
                             f"Ваше имя: {user_info['user_name']}\n"
                             f"Ваша фамилия: {user_info['user_last_name']}\n\n"
                             f"Все верно? 🤔", reply_markup=confirmation_menu)
        await register.user_answer.set()


@dp.message_handler(state=register.user_numbers_groups)
async def register_step_numbers_groups(message: types.Message, state: FSMContext):
    if not DataBase.get_check_group(message.text):
        await message.answer("Такой группы нет повторите попытку")
        return
    else:
        await state.update_data(user_numbers_groups=message.text)
        user_info = await state.get_data()
        await message.answer(f"Ваша должность: {user_info['user_status']}\n"
                             f"Ваше имя: {user_info['user_name']}\n"
                             f"Ваша фамилия: {user_info['user_last_name']}\n"
                             f"Ваша группа: {user_info['user_numbers_groups']}\n\n"
                             f"Все верно? 🤔", reply_markup=confirmation_menu)
        await register.user_answer.set()


@dp.message_handler(state=register.user_answer)
async def register_step_answer(message: types.Message, state: FSMContext):
    if message.text == "Да ✅":
        await message.answer("Регистрация прошла успешно ✅", reply_markup=types.ReplyKeyboardRemove())
        user_info = await state.get_data()
        if user_info['user_status'] == "Студент":
            print(user_info)
            DataBase.set_user_data_json(user_id=user_info['user_id'], user_status=user_info['user_status'],
                                        user_name=user_info['user_name'], user_last_name=user_info['user_last_name'],
                                        user_group=user_info['user_numbers_groups'])
            await state.finish()
        elif user_info['user_status'] == "Преподаватель":
            await message.answer("Для завершения регистрации вам нужно подтвердить почту")
            await state.finish()
    elif message.text == "Нет ❌":
        await message.answer("Вы начинаете регистрацию заново")
        await message.answer("Ваша должность?", reply_markup=status_menu)
        await register.user_status.set()


# Todo ------------------------------------------- Lessons Branch -----------------------------------------------------
@dp.message_handler(Command('les'))
async def les_step_start(message: types.Message):
    await message.answer('Выбирайте', reply_markup=KeyBoard.les_menu)
    await lessons.user_answer_les_start.set()


@dp.message_handler(state=lessons.user_answer_les_start)
async def les_menu(message: types.Message, state: FSMContext):
    if DataBase.get_availability_user(message.from_user.id) == 0:
        if message.text == "Ваше расписание":
            await message.answer("Выбирайте", reply_markup=KeyBoard.your_less_menu)
            await lessons.user_answer_your_les.set()
        elif message.text == "Расписание преподавателя":
            await message.answer("Находится в стадии доработки\n\n "
                                 "P.s Примерное добавление в конце апреля")
            return
        elif message.text == "Расписание по номеру группы":
            await message.answer("Введите номер академической группы")
            await lessons.user_answer_number_les.set()
        elif message.text == "Выйти":
            await message.answer("Выход", reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
    else:
        await message.answer("Упс... 😕\n"
                             "Для того, чтобы пользоваться расписанием, вам надо зарегистрироваться\n"
                             "Команда для регистрации: /reg")
        await state.finish()


@dp.message_handler(state=lessons.user_answer_your_les)
async def your_les_menu(message: types.Message, state: FSMContext):
    if DataBase.get_check_user_status(message.from_user.id) == "Студент":
        if message.text == "Вчера":
            list_les = Lessons.get_schedule_students(DataBase.get_check_numbers_user(message.from_user.id),
                                                     Data_work.get_back_data())
            if len(list_les) == 0:
                await message.answer(f"Вы выбрали: Вчера\n"
                                     f"Сейчас {Data_work.get_now_time()} {Data_work.get_now_data()}\n\n"
                                     f"Выходной 🎉", parse_mode=types.ParseMode.HTML)
            else:
                result = []
                for i in range(len(list_les)):
                    result.append(" ".join(list_les[i]))
                    result[i] = str(result[i]) + '\n\n'
                await message.answer(f"Вы выбрали: Вчера\n"
                                     f"Сейчас {Data_work.get_now_time()} {Data_work.get_now_data()}\n\n"
                                     f"{''.join(result)}", parse_mode=types.ParseMode.HTML)
            return
        elif message.text == "Сегодня":
            list_les = Lessons.get_schedule_students(DataBase.get_check_numbers_user(message.from_user.id),
                                                     Data_work.get_now_data())
            if len(list_les) == 0:
                await message.answer(f"Вы выбрали: Сегодня\n"
                                     f"Сейчас {Data_work.get_now_time()} {Data_work.get_now_data()}\n\n"
                                     f"Выходной 🎉", parse_mode=types.ParseMode.HTML)
            else:
                result = []
                for i in range(len(list_les)):
                    result.append(" ".join(list_les[i]))
                    result[i] = str(result[i]) + '\n\n'
                await message.answer(f"Вы выбрали: Сегодня\n"
                                     f"Сейчас {Data_work.get_now_time()} {Data_work.get_now_data()}\n\n"
                                     f"{''.join(result)}", parse_mode=types.ParseMode.HTML)
            return
        elif message.text == "Завтра":
            list_les = Lessons.get_schedule_students(DataBase.get_check_numbers_user(message.from_user.id),
                                                     Data_work.get_next_data())
            if len(list_les) == 0:
                await message.answer(f"Вы выбрали: Завтра\n"
                                     f"Сейчас {Data_work.get_now_time()}\n\n"
                                     f"Выходной 🎉", parse_mode=types.ParseMode.HTML)
            else:
                result = []
                for i in range(len(list_les)):
                    result.append(" ".join(list_les[i]))
                    result[i] = str(result[i]) + '\n\n'
                await message.answer(f"Вы выбрали: Завтра\n"
                                     f"Сейчас {Data_work.get_now_time()} {Data_work.get_now_data()}\n\n"
                                     f"{''.join(result)}", parse_mode=types.ParseMode.HTML)
            return
        elif message.text == "Назад":
            await message.answer("Назад", reply_markup=KeyBoard.les_menu)
            await lessons.user_answer_les_start.set()
    else:
        await message.answer("Находится в стадии разработки")
        await state.finish()


@dp.message_handler(state=lessons.user_answer_number_les)
async def number_les(message: types.Message, state: FSMContext):
    if DataBase.get_check_group(message.text):
        await state.update_data(number_group=message.text)
        await message.answer("Выбирайте", reply_markup=KeyBoard.your_less_menu)
        await lessons.user_answer_number_les2.set()
    else:
        await message.answer("Упс... 😕\n"
                             "Такой группы нет в каи, попробуйте снова")


@dp.message_handler(state=lessons.user_answer_number_les2)
async def number_les2(message: types.Message, state: FSMContext):
    number_groups = await state.get_data()
    if message.text == "Вчера":
        list_les = Lessons.get_schedule_students(number_groups['number_group'],
                                                 Data_work.get_back_data())
        if len(list_les) == 0:
            await message.answer(f"Вы выбрали: Группу {number_groups['number_group']} Вчера\n"
                                 f"Сейчас {Data_work.get_now_time()} {Data_work.get_now_data()}\n\n"
                                 f"Выходной 🎉", parse_mode=types.ParseMode.HTML)
        else:
            result = []
            for i in range(len(list_les)):
                result.append(" ".join(list_les[i]))
                result[i] = str(result[i]) + '\n\n'
            await message.answer(f"Вы выбрали: Группу {number_groups['number_group']} Вчера\n"
                                 f"Сейчас {Data_work.get_now_time()} {Data_work.get_now_data()}\n\n"
                                 f"{''.join(result)}", parse_mode=types.ParseMode.HTML)
        return
    elif message.text == "Сегодня":
        list_les = Lessons.get_schedule_students(number_groups['number_group'],
                                                 Data_work.get_now_data())
        if len(list_les) == 0:
            await message.answer(f"Вы выбрали: Группу {number_groups['number_group']} Сегодня\n"
                                 f"Сейчас {Data_work.get_now_time()} {Data_work.get_now_data()}\n\n"
                                 f"Выходной 🎉", parse_mode=types.ParseMode.HTML)
        else:
            result = []
            for i in range(len(list_les)):
                result.append(" ".join(list_les[i]))
                result[i] = str(result[i]) + '\n\n'
            await message.answer(f"Вы выбрали: Группу {number_groups['number_group']} Сегодня\n"
                                 f"Сейчас {Data_work.get_now_time()} {Data_work.get_now_data()}\n\n"
                                 f"{''.join(result)}", parse_mode=types.ParseMode.HTML)
        return
    elif message.text == "Завтра":
        list_les = Lessons.get_schedule_students(number_groups['number_group'],
                                                 Data_work.get_next_data())
        if len(list_les) == 0:
            await message.answer(f"Вы выбрали: Группу {number_groups['number_group']} Завтра\n"
                                 f"Сейчас {Data_work.get_now_time()}\n\n"
                                 f"Выходной 🎉", parse_mode=types.ParseMode.HTML)
        else:
            result = []
            for i in range(len(list_les)):
                result.append(" ".join(list_les[i]))
                result[i] = str(result[i]) + '\n\n'
            await message.answer(f"Вы выбрали: Группу {number_groups['number_group']} Завтра\n"
                                 f"Сейчас {Data_work.get_now_time()} {Data_work.get_now_data()}\n\n"
                                 f"{''.join(result)}", parse_mode=types.ParseMode.HTML)
        return
    elif message.text == "Назад":
        await message.answer("Назад", reply_markup=KeyBoard.les_menu)
        await lessons.user_answer_les_start.set()


# Todo --------------------------------- Report Branch ---------------------------------------------------------------
@dp.message_handler(Command("report"))
async def report_start(message: types.Message):
    await message.answer('Подробно опишите проблему\n\n'
                         'P.S Заранее благодарим за помощь 🤩')
    await report.user_report.set()


@dp.message_handler(state=report.user_report)
async def report_message(message: types.Message, state: FSMContext):
    await message.answer("Сообщение об ошибке было отправлено")
    DataBase.set_user_report(message.from_user.id, message.text,
                             f"{Data_work.get_now_data()} {Data_work.get_now_time()}")
    await state.finish()

# Todo ------------------------------------ Week Branch --------------------------------------------------------------
@dp.message_handler(Command("week"))
async def week_command(message : types.Message):
    if Data_work.get_parity_week(Data_work.get_now_data()) == "Четная":
        await message.answer()