import csv
import json
from Data import DataBase
from LocalDataLessons import Lessons
from Lib import Data_work
from datetime import datetime
#
# l = list()
# with open("LocalDataLessons/09-03-03_even.csv", "r", newline='', encoding="utf-8") as file_r:
#     dd = csv.DictReader(file_r, delimiter='|')
#     for row in dd:
#         if row["0"] == Data_work.get_convert_week(Data_work.get_now_data()):
#             for i in range(8 - 1):
#                 try:
#                     l.append([row[],row[f"{i}"]])
#                 except KeyError:
#                     break
#             # try:
#             #     l.append(row["9"])
#             # except KeyError:
#             #     print("Такого ключа нет")
#             #     break
#             # l.append(row["9"])
#
# print(l)
#
# with open("Data/dict_group.json", "r", encoding="utf-8") as file_r:
#     dict_groups = json.load(file_r)
#
# with open("LocalDataLessons/09-03-03_even.csv", "r", newline="", encoding="utf-8") as file_r:
#     l = list()
#     find = "Мочелевская"
#     i = 0
#     dd = csv.DictReader(file_r, delimiter="|")
#     for row in dd:
#         for i in range(8):
#             try:
#                 if Data_work.get_convert_week(Data_work.get_now_data()) == row['0']:
#                     if find in row[f"{i}"]:
#                         l.append([row[f"{i-1}"], row[f"{i}"]])
#             except KeyError:
#                 break
#     print(l)


list_groups = list()
list_schedule = list()
with open("Data/dict_group.json", "r", encoding="utf-8") as file_r:
    dict_group = json.load(file_r)
for key in dict_group:
    list_groups.append(key)
if Data_work.get_parity_week() == "Четная":
    for groups in list_groups:
        with open(f"LocalDataLessons/{groups}_even.csv", "r", newline="", encoding="utf-8") as file_even:
            even = csv.DictReader(file_even, delimiter="|")
            for row in even:
                for i in range(8):
                    try:
                        if Data_work.get_convert_week(Data_work.get_now_data()) == row["0"]:
                            if "Мочелевская" in row[f"{i}"]:
                                list_schedule.append([row[f"{i - 1}"], row[f"{i}"]])
                    except KeyError:
                        break
print(list_schedule)
print(list_groups)

# print(Data_work.get_convert_week(Data_work.get_now_data()))
# print(Lessons.get_schedule_teacher("Мочелевская", Data_work.get_now_data()))
