import asyncio
import time
import threading
import colorama
import LocalDataLessons
import pytz

from datetime import datetime
from Lib import Data_work
from Config import config
from Loader import storage
from colorama import Fore
from aiogram import Bot, Dispatcher, executor

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

        if datetime.now(tz=pytz.timezone("Europe/Moscow")).time().hour == 14:
            LocalDataLessons.Parse.set_schedule()
            print(Fore.GREEN + f"|{Data_work.get_now_time()}|" + Fore.LIGHTWHITE_EX + "|Расписание обновлено|")
            time.sleep(3600)
        else:
            print(Fore.RED + f"|{Data_work.get_now_time()}|" + Fore.LIGHTWHITE_EX + "|Расписание не обновлено|")
            time.sleep(3600)


# TODO ------------------------------------------ Main ----------------------------------------------------------------

if __name__ == "__main__":
    from hand import dp, get_default_commands

    threading_update = threading.Thread(target=update_local_lessons)
    threading_update.start()

    print(Fore.GREEN + f"|{Data_work.get_now_time()}|" + Fore.LIGHTWHITE_EX + "|Бот запущен|")
    executor.start_polling(dp, on_startup=get_default_commands)
