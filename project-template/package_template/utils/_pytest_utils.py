"""
This module provide a function to test logging functions
"""
import os


def check_log(class_func: str):
    cur_path = os.path.dirname(os.path.abspath(__file__))
    log_folder_index = cur_path.rfind("/", 0, cur_path.rfind("/"))
    log_path = cur_path[:log_folder_index] + "/log/pyspark_info.log"

    with open(log_path) as f:
        f = f.readlines()

    start = False
    duration = False
    finish = False

    for line in f:
        if line.find(f"{class_func} starts running") != -1:
            start = True
        if line.find(f"{class_func} lasts for") != -1:
            duration = True
        if line.find(f"{class_func} ends running") != -1:
            finish = True

    return start and finish and duration
