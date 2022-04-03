from lxml import etree

from backend.control.util.log_util import log_error


def get_html_root(file_path):
    try:
        ps = etree.HTMLParser()
        tr = etree.parse(file_path, ps)
        return tr.getroot()
    except Exception as ex:
        log_error("Failed to parse the HTML file \"{}\"! Reason: {}".format(file_path, str(ex)))
        return None
