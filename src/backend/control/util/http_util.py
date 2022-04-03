import os

import requests

from backend.control.util.log_util import log_debug, log_error
from main.global_vars import status_info


def download_text(url, file_path):
    if os.path.exists(file_path):
        return True

    # Download the web page to a local file.
    msg = "Download \"{}\"...".format(url)
    log_debug(msg)
    status_info(msg)
    try:
        resp = requests.get(url)
        if not resp.ok:
            log_error("Failed to download the web page \"{}\"! Status code: {}".format(url, resp.status_code))
            return False

        with open(file_path, "w") as fh:
            fh.write(resp.text)
        return True
    except Exception as ex:
        log_error("Failed to download the web page from \"{}\"! Reason: {}".format(url, str(ex)))
        return False


def download_pdf(url, file_path):
    return download_binary(url, file_path)


def download_mp3(url, file_path):
    return download_binary(url, file_path)


def download_binary(url, file_path):
    if os.path.exists(file_path):
        return True

    # Download the web page to a local file.
    msg = "Download \"{}\"...".format(url)
    log_debug(msg)
    status_info(msg)
    try:
        resp = requests.get(url)
        if not resp.ok:
            log_error("Failed to download the web page \"{}\" for \"{}\"! Status code: {}"
                      .format(url, file_path, resp.status_code))
            return False

        with open(file_path, "wb") as fh:
            fh.write(resp.content)
        return True
    except Exception as ex:
        log_error("Failed to download the binary for \"{}\" with URL \"{}\"! Reason: {}"
                  .format(file_path, url, str(ex)))
        return False


def extract_h2_from_anchor_element(anchor):
    h2_list = anchor.xpath("./h2")
    if not len(h2_list) > 0:
        return ""
    h2 = h2_list[0]
    return h2.text.strip()


def extract_tail_text(anchor):
    h2_list = anchor.xpath("./h2")
    if not len(h2_list) > 0:
        return ""

    for h2 in h2_list:
        for child in h2:
            txt = child.tail.strip()
            if len(txt) > 0:
                return txt
    return ""
