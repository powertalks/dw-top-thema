import json

from backend.control.util.log_util import log_error


def save_to_json_file(obj, output_file):
    try:
        with open(output_file, "w") as fh:
            json.dump(obj, fh)
        return True
    except Exception as ex:
        log_error("Failed to save to JSON file \"{}\"! Reason: {}".format(output_file, str(ex)))
        return False


def load_from_json_file(input_file):
    try:
        with open(input_file, "r") as fh:
            obj = json.load(fh)
            return obj
    except Exception as ex:
        log_error("Failed to load from JSON file \"{}\"! Reason: {}".format(input_file, str(ex)))
        return None
