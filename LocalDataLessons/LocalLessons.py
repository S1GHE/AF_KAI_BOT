import csv
import json

import pandas as pd

from Config import config
from Lib import Data_work, Support_def
from Data import DataBase


# TODO ---------------------------------------- Parse -----------------------------------------------------------------
class Parse:

    @staticmethod
    def set_schedule():
        table = pd.read_html(config.url_090301_even_week, encoding="utf-8")[0]
        table.to_csv('LocalDataLessons/09-03-01_even.csv', sep='|', index=False)

        table = pd.read_html(config.url_090301_odd_week, encoding='utf-8')[0]
        table.to_csv('LocalDataLessons/09-03-01_odd.csv', sep='|', index=False)

        table = pd.read_html(config.url_090903_odd_week, encoding='utf-8')[0]
        table.to_csv('LocalDataLessons/09-03-03_odd.csv', sep='|', index=False)

        table = pd.read_html(config.url_090903_even_week, encoding='utf-8')[0]
        table.to_csv('LocalDataLessons/09-03-03_even.csv', sep='|', index=False)

        table = pd.read_html(config.url_150305_even_week, encoding='utf-8')[0]
        table.to_csv('LocalDataLessons/15-03-05_even.csv', sep='|', index=False)

        table = pd.read_html(config.url_150305_odd_week, encoding='utf-8')[0]
        table.to_csv('LocalDataLessons/15-03-05_odd.csv', sep='|', index=False)

        table = pd.read_html(config.url_200301_even_week, encoding='utf-8')[0]
        table.to_csv('LocalDataLessons/20-03-01_even.csv', sep='|', index=False)

        table = pd.read_html(config.url_200301_odd_week, encoding='utf-8')[0]
        table.to_csv('LocalDataLessons/20-03-01_odd.csv', sep='|', index=False)

        table = pd.read_html(config.url_380301_odd_week, encoding='utf-8')[0]
        table.to_csv('LocalDataLessons/38-03-01_odd.csv', sep='|', index=False)

        table = pd.read_html(config.url_380301_even_week, encoding='utf-8')[0]
        table.to_csv('LocalDataLessons/38-03-01_even.csv', sep='|', index=False)


# TODO ---------------------------------- Local Lessons --------------------------------------------------------------
class Lessons:

    @staticmethod
    def get_schedule_students(num_groups, data):

        list_schedule = list()
        new_list_schedule = list()

        if Data_work.get_parity_week(data) == "Четная":
            with open(f"LocalDataLessons/{DataBase.get_check_group(num_groups)}_even.csv", "r", newline="",
                      encoding="utf-8") as file_even:
                even_week = csv.DictReader(file_even, delimiter="|")
                if "7" in num_groups:
                    if num_groups.find("2", 2, 4) == 2:
                        for row in even_week:
                            if row["0"] == Data_work.get_convert_week(data):
                                list_schedule.append([row["1"], row["2"]])
                    elif num_groups.find("3", 2, 4) == 2:
                        for row in even_week:
                            if row["0"] == Data_work.get_convert_week(data):
                                list_schedule.append([row["3"], row["4"]])
                    elif num_groups.find("4", 2, 4) == 2:
                        for row in even_week:
                            if row["0"] == Data_work.get_convert_week(data):
                                list_schedule.append([row["5"], row["6"]])
                else:
                    if num_groups.find("1", 2, 4) == 2:
                        for row in even_week:
                            if row["0"] == Data_work.get_convert_week(data):
                                list_schedule.append([row["1"], row["2"]])
                    elif num_groups.find("2", 2, 4) == 2:
                        for row in even_week:
                            if row["0"] == Data_work.get_convert_week(data):
                                list_schedule.append([row["3"], row["4"]])
                    elif num_groups.find("3", 2, 4) == 2:
                        for row in even_week:
                            if row["0"] == Data_work.get_convert_week(data):
                                list_schedule.append([row["5"], row["6"]])
                    elif num_groups.find("4", 2, 4) == 2:
                        for row in even_week:
                            if row["0"] == Data_work.get_convert_week(data):
                                list_schedule.append([row["7"], row["8"]])

        else:
            with open(f"LocalDataLessons/{DataBase.get_check_group(num_groups)}_odd.csv", "r", newline="",
                      encoding="utf-8") as file_odd:
                odd_week = csv.DictReader(file_odd, delimiter="|")
                if "7" in num_groups:
                    if num_groups.find("2", 2, 4) == 2:
                        for row in odd_week:
                            if row["0"] == Data_work.get_convert_week(data):
                                list_schedule.append([row["1"], row["2"]])
                    elif num_groups.find("3", 2, 4) == 2:
                        for row in odd_week:
                            if row["0"] == Data_work.get_convert_week(data):
                                list_schedule.append([row["3"], row["4"]])
                    elif num_groups.find("4", 2, 4) == 2:
                        for row in odd_week:
                            if row["0"] == Data_work.get_convert_week(data):
                                list_schedule.append([row["5"], row["6"]])
                else:
                    if num_groups.find("1", 2, 4) == 2:
                        for row in odd_week:
                            if row["0"] == Data_work.get_convert_week(data):
                                list_schedule.append([row["1"], row["2"]])
                    elif num_groups.find("2", 2, 4) == 2:
                        for row in odd_week:
                            if row["0"] == Data_work.get_convert_week(data):
                                list_schedule.append([row["3"], row["4"]])
                    elif num_groups.find("3", 2, 4) == 2:
                        for row in odd_week:
                            if row["0"] == Data_work.get_convert_week(data):
                                list_schedule.append([row["5"], row["6"]])
                    elif num_groups.find("4", 2, 4) == 2:
                        for row in odd_week:
                            if row["0"] == Data_work.get_convert_week(data):
                                list_schedule.append([row["7"], row["8"]])

        for c_list in list_schedule:
            if not Support_def.check_str_empty(c_list):
                new_list_schedule.append(c_list)

        return new_list_schedule

    @staticmethod
    def get_schedule_teacher(last_name, data):
        pass
        # list_groups = list()
        # list_schedule = list()
        # with open("Data/dict_group.json", "r", encoding="utf-8") as file_r:
        #     dict_group = json.load(file_r)
        # for key in dict_group:
        #     list_groups.append(key)
        # if Data_work.get_parity_week() == "Четная":
        #     for groups in list_groups:
        #         with open(f"LocalDataLessons/{groups}_even.csv", "r", newline="", encoding="utf-8") as file_even:
        #             even = csv.DictReader(file_even, delimiter="|")
        #         for row in even:
        #             for i in range(8):
        #                 try:
        #                     if Data_work.get_convert_week(data) == row["0"]:
        #                         if last_name in row[f"{i}"]:
        #                             list_schedule.append([row[f"{i-1}"], row[f"{i}"]])
        #                 except KeyError:
        #                     break
        # else:
        #     for groups in list_groups:
        #         with open(f"LocalDataLessons/{groups}_odd.csv", "r", newline="", encoding="utf-8") as file_even:
        #             odd = csv.DictReader(file_even, delimiter="|")
        #         for row in odd:
        #             for i in range(8):
        #                 try:
        #                     if Data_work.get_convert_week(data) == row["0"]:
        #                         if last_name in row[f"{i}"]:
        #                             list_schedule.append([row[f"{i-1}"], row[f"{i}"]])
        #                 except KeyError:
        #                     break
        #
        # return list_schedule

