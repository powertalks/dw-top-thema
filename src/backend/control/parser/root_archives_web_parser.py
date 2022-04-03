import re

from backend.control.util.http_util import extract_h2_from_anchor_element
from backend.control.util.log_util import log_error
from backend.control.util.xml_util import get_html_root


class RootArchivesWebParser(object):

    def __init__(self, input_file):
        self.input_file = input_file

    def extract(self):
        url_dict = dict()
        try:
            # Parse the URL of each archive page.
            html_root = get_html_root(self.input_file)
            xpath_text = "//div[@id='bodyContent']"
            xpath_text += "/div[@class='col2 left']"
            xpath_text += "/div[@class='col2 articleDetailTeaser']"
            xpath_text += "/div[@class='group']"
            xpath_text += "/div[@class='linkList intern']/a"
            anchor_list = html_root.xpath(xpath_text)
            pattern = re.compile(r"^Top-Thema mit Vokabeln – Archiv (\d{4})$")
            for anchor in anchor_list:
                url = anchor.attrib["href"].strip()
                txt = extract_h2_from_anchor_element(anchor)
                if not len(txt) > 0:
                    log_error("Failed to parse text from an anchor element! File: {}".format(self.input_file))
                    return None

                match = pattern.match(txt)
                if match is not None:
                    url_dict[match.group(1)] = url
                else:
                    log_error("Unexpected text \"{}\" when parsing archive URL! File: {}".format(txt, self.input_file))
                    return None
        except Exception as ex:
            log_error("Failed to parse the archives web! File: {}".format(self.input_file))
            return None
        return url_dict
