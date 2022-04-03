import glob
import os

from backend.control.util.report_util import show_error
from main.global_vars import g_date_format


def file_exists(file_path):
    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            return True
    return False


# Make sure that the given directory exists.
def validate_dir(dir_path):
    if os.path.exists(dir_path):
        if os.path.isdir(dir_path):
            return True
        else:
            show_error("The application expects a directory under the path \"{}\"!".format(dir_path))
            return False
    else:
        try:
            os.makedirs(dir_path)
            return True
        except Exception as ex:
            show_error("Failed to create the directory \"{}\"! Reason: {}".format(dir_path, str(ex)))
            return False


def get_file_list(dir_path, pattern):
    pttn = "{}/*.html".format(dir_path, pattern)
    file_list = glob.glob(pttn)
    return file_list


def build_file_path(dir_path, dt, web_file_path, file_type, ext_name):
    dt_txt = dt.strftime(g_date_format)
    base_name = os.path.basename(web_file_path)
    tmp = os.path.splitext(base_name)
    if len(file_type) > 0:
        file_name = "{}_{}_{}.{}".format(dt_txt, tmp[0], file_type, ext_name)
    else:
        file_name = "{}_{}.{}".format(dt_txt, tmp[0], ext_name)
    file_path = os.path.join(dir_path, file_name)
    return file_path
