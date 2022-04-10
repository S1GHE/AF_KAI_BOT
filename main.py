import asyncio
import time
import threading

import aiogram.utils.exceptions
import colorama
import LocalDataLessons
import pytz

from LocalDataLessons import Lessons
from Data import DataBase
from datetime import datetime
from Lib import Data_work
from Config import config
from Loader import storage
from colorama import Fore
from aiogram import Bot, Dispatcher, executor , types

colorama.init()

loop = asyncio.get_event_loop()
bot = Bot(config.bot_token)
dp = Dispatcher(bot, loop=loop, storage=storage)


# TODO --------------------------------------- Update Local Lessons ---------------------------------------------------
def update_local_lessons():
    """
    Обновление расписания
    :return:
    """
    while True:

        if datetime.now(tz=pytz.timezone("Europe/Moscow")).time().hour == 0:
            LocalDataLessons.Parse.set_schedule()
            print(Fore.GREEN + f"|{Data_work.get_now_time()}|" + Fore.LIGHTWHITE_EX + "|Расписание обновлено|")
            time.sleep(3600)
        else:
            print(Fore.RED + f"|{Data_work.get_now_time()}|" + Fore.LIGHTWHITE_EX + "|Расписание не обновлено|")
            time.sleep(3600)


# TODO ---------------------------------------- Auto Mail -------------------------------------------------------------

async def periodic_auto_mail(sleep_for):
    """
    Рассылка расписания в 20:00 по мск всем пользователям
    :param sleep_for:
    :return:
    """
    while True:
        if datetime.now(tz=pytz.timezone("Europe/Moscow")).time().hour == 5:
            for user_id in DataBase.get_all_id():
                list_les = Lessons.get_schedule_students(DataBase.get_check_numbers_user(user_id),
                                                         Data_work.get_next_data())
                if len(list_les) == 0:
                    try:
                        await bot.send_message(text=f"<b>Сегодня "
                                                    f"Дата: {Data_work.get_now_data()} "
                                                    f"Время: {Data_work.get_now_time()}</b>"
                                                    f"\n\n"
                                                    f"Твоё расписание на завтра\n"
                                                    f"Выходной 🎉", chat_id=user_id, parse_mode=types.ParseMode.HTML)
                    except aiogram.utils.exceptions.BotBlocked:
                        pass
                else:
                    try:
                        result = list()
                        for i in range(len(list_les)):
                            result.append(" ".join(list_les[i]))
                            result[i] = str(result[i]) + '\n\n'
                        await bot.send_message(text=f"<b>Сегодня "
                                                    f"Дата: {Data_work.get_now_data()} "
                                                    f"Время: {Data_work.get_now_time()}</b>"
                                                    f"\n\n"
                                                    f"<b>Твоё расписание на завтра:</b>\n"
                                                    f"{''.join(result)}", chat_id=user_id,
                                                    parse_mode=types.ParseMode.HTML)
                    except aiogram.utils.exceptions.BotBlocked:
                        pass
            print(Fore.GREEN + f"|{Data_work.get_now_time()}|" + Fore.LIGHTWHITE_EX + "|Рассылка была отправлена|")
        else:
            print(Fore.RED + f"|{Data_work.get_now_time()}|" + Fore.LIGHTWHITE_EX + "|Рассылка не была отправлена|")
        await asyncio.sleep(sleep_for)

# TODO ------------------------------------------ Main ----------------------------------------------------------------

if __name__ == "__main__":
    from hand import dp, get_default_commands

    threading_update = threading.Thread(target=update_local_lessons)
    threading_update.start()

    dp.loop.create_task(periodic_auto_mail(3600))

    print(Fore.GREEN + f"|{Data_work.get_now_time()}|" + Fore.LIGHTWHITE_EX + "|Бот запущен|")
    executor.start_polling(dp, on_startup=get_default_commands)
