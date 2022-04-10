import csv
import json
from Lib import Support_def


class DataBase:

    # TODO ------------------------------------ Set Data Base --------------------------------------------------------
    @staticmethod
    def set_user_data_json(user_id, user_name, user_last_name, user_status, user_group):
        """
        Добавляет пользователя в базу данных
        :param user_id:
        :param user_name:
        :param user_last_name:
        :param user_status:
        :param user_group:
        :return:
        """
        dict_set_user = {
            str(user_id): [str(user_name), str(user_last_name), str(user_status), str(user_group), str(1)]}
        with open("Data/user_data.json", "r", encoding="utf-8") as file_json_r:
            dict_get_user_last_db = json.load(file_json_r)
        dict_set_user_new = Support_def.sum_dict(dict_get_user_last_db, dict_set_user)
        with open("Data/user_data.json", "w", encoding="utf-8") as file_json_w:
            json.dump(dict_set_user_new, file_json_w, indent=4, ensure_ascii=False)

    @staticmethod
    def set_user_report(user_id, user_message, data_report):
        with open("Data/report_user.csv", "a", encoding="utf-8", newline='') as file_csv:
            report = csv.writer(file_csv, delimiter="|", lineterminator="\r")
            report.writerow([user_id, user_message, data_report])

    # TODO ------------------------------------ Get Data Base --------------------------------------------------------
    @staticmethod
    def get_check_group(numb_groups):
        """
        Проверяет наличие данной группы в каи
        :param numb_groups:
        :return:
        """
        with open("Data/dict_group.json", "r", encoding="utf-8") as file_r:
            dict_get_group = json.load(file_r)
        for key in dict_get_group:
            for i in dict_get_group[key]:
                if i == str(numb_groups):
                    return key

        return False

    @staticmethod
    def get_availability_user(user_id):
        """
        Проверяет наличе пользователя в базе данных
        :param user_id:
        :return:
        """
        with open("Data/user_data.json", "r", encoding="utf-8") as file_r:
            dict_get_user = json.load(file_r)
            for key in dict_get_user:
                if key == str(user_id):
                    return 0

        return 1

    @staticmethod
    def get_check_user_status(user_id):
        """
        Проверяет должность пользователя
        :param user_id:
        :return:
        """
        with open("Data/user_data.json", "r", encoding="utf-8") as file_r:
            dict_get_user = json.load(file_r)
            for key in dict_get_user:
                if dict_get_user[key][2] == "Студент":
                    return dict_get_user[key][2]
                elif dict_get_user[key][2] == "Преподаватель":
                    return dict_get_user[key][2]

    @staticmethod
    def get_check_numbers_user(user_id):
        """
        Проверяет номер группы пользователя
        :param user_id:
        :return:
        """
        with open("Data/user_data.json", "r", encoding="utf-8") as file_r:
            dict_get_user = json.load(file_r)
            for key in dict_get_user:
                if str(user_id) == key:
                    return dict_get_user[key][3]

    @staticmethod
    def get_all_id():
        """
        Получает все ID пользователей
        :return:
        """
        user_id_list = list()
        with open("Data/user_data.json", "r", encoding="utf-8") as file_r:
            dict_get_all_id = json.load(file_r)
            for key in dict_get_all_id:
                user_id_list.append(key)

        return user_id_list
