import os
from datetime import datetime

from main.global_vars import status_error, status_info, status_warning

g_start_time = ""


def log_error(msg):
    write_to_log_file("error", msg)
    status_error(msg)
    ts = get_time_stamp_for_message()
    print("# {} # error # {}".format(ts, msg))


def log_warning(msg):
    write_to_log_file("warning", msg)
    status_warning(msg)
    ts = get_time_stamp_for_message()
    print("# {} # warning # {}".format(ts, msg))


def log_info(msg):
    write_to_log_file("info", msg)
    status_info(msg)


def log_debug(msg):
    write_to_log_file("debug", msg)


def write_to_log_file(msg_type, msg_text):
    ts_file = get_time_stamp_for_file_name()
    file_name = "{}.log".format(ts_file)
    dir_log = r"D:\dev\pycharm\dw-top-thema2\log"
    file_path = os.path.join(dir_log, file_name)
    ts_msg = get_time_stamp_for_message()
    with open(file_path, "a") as fh:
        txt = "# {} # {} # {}\n".format(ts_msg, msg_type, msg_text)
        fh.write(txt)


def get_time_stamp_for_file_name():
    global g_start_time
    if not len(g_start_time) > 0:
        dt = datetime.now()
        g_start_time = dt.strftime("%Y-%m-%d_%H-%M-%S_%f")
    return g_start_time


def get_time_stamp_for_message():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
