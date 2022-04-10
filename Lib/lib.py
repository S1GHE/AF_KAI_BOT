from datetime import datetime, timedelta


# todo --------------------------------- class Support_def ------------------------------------------------------------
class Support_def:

    @staticmethod
    def sum_dict(dict_1, dict_2):
        """
        Складывает два словаря
        :param dict_1:
        :param dict_2:
        :return:
        """
        i = 0
        items = list()
        keys = list()
        result_dict = dict()
        for key in dict_1:
            keys.append(key)
        for key in dict_2:
            keys.append(key)
        for item in dict_1:
            items.append(dict_1[item])
        for item in dict_2:
            items.append(dict_2[item])
        for key in range(len(items)):
            result_dict[keys[i]] = items[i]
            i += 1

        return result_dict

    @staticmethod
    def check_str_empty(c_list):
        """
        Проверка на наличие пустых строк в списке
        :param c_list:
        :return:
        """
        for i in c_list:
            if not i:
                return True
        return False


# todo ----------------------------------- class Data_work ------------------------------------------------------------
class Data_work:
    today = datetime.today() + timedelta(hours=3)

    @staticmethod
    def get_parity_week(data):
        """
        Определяет четность/нечетность недели
        :return:
        """

        num_week_now = datetime.strptime(data, "%d.%m.%y").isocalendar()[1]
        if int(num_week_now) % 2 == 0:
            return "Четная"
        else:
            return "Нечетная"

    @staticmethod
    def get_now_time():
        """
        Получаем текущее время
        :return:
        """
        now_time = Data_work.today.strftime("%H:%M:%S")

        return now_time

    @staticmethod
    def get_now_data():
        """
        Получаем текущую дату
        :return:
        """
        now_data = Data_work.today.strftime("%d.%m.%y")

        return now_data

    @staticmethod
    def get_next_data():
        """
        Получает завтрашнюю дату
        :return:
        """
        day = Data_work.today + timedelta(days=1)
        next_data = day.strftime("%d.%m.%y")

        return next_data

    @staticmethod
    def get_back_data():
        """
        Получает вчерашнюю дату
        :return:
        """
        day = Data_work.today + timedelta(days=-1)
        back_data = day.strftime("%d.%m.%y")

        return back_data

    @staticmethod
    def get_convert_week(data):
        """
        Конвертирует формат даты, так как в таблице
        :param data:
        :return:
        """
        days = ""
        if datetime.strptime(data, "%d.%m.%y").weekday() == 0:
            days = "Понедельник" + datetime.strptime(data, "%d.%m.%y").strftime("%d.%m")
        elif datetime.strptime(data, "%d.%m.%y").weekday() == 1:
            days = "Вторник" + datetime.strptime(data, "%d.%m.%y").strftime("%d.%m")
        elif datetime.strptime(data, "%d.%m.%y").weekday() == 2:
            days = "Среда" + datetime.strptime(data, "%d.%m.%y").strftime("%d.%m")
        elif datetime.strptime(data, "%d.%m.%y").weekday() == 3:
            days = "Четверг" + datetime.strptime(data, "%d.%m.%y").strftime("%d.%m")
        elif datetime.strptime(data, "%d.%m.%y").weekday() == 4:
            days = "Пятница" + datetime.strptime(data, "%d.%m.%y").strftime("%d.%m")
        elif datetime.strptime(data, "%d.%m.%y").weekday() == 5:
            days = "Суббота" + datetime.strptime(data, "%d.%m.%y").strftime("%d.%m")
        elif datetime.strptime(data, "%d.%m.%y").weekday() == 6:
            days = "Воскресенье" + datetime.strptime(data, "%d.%m.%y").strftime("%d.%m")

        return days
