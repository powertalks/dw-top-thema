import re

from backend.control.util.http_util import extract_h2_from_anchor_element, extract_tail_text
from backend.control.util.xml_util import get_html_root


class YearlyArchivesWebParser(object):

    def __init__(self, input_file):
        self.input_file = input_file

    def extract(self):
        url_dict = dict()
        try:
            # Parse the URL of each archive page.
            rt = get_html_root(self.input_file)
            anchor_list = rt.xpath("//div[@class=\"linkList intern\"]/a")
            pattern = re.compile(r"[^0-9a-zA-Z\-]")
            for anchor in anchor_list:
                url = anchor.attrib["href"].strip()
                txt = extract_h2_from_anchor_element(anchor)

                # The text of the h2 element may be empty, i.e. for year 2020.
                if not len(txt) > 0:
                    txt = extract_tail_text(anchor)

                txt = re.sub("[äÄ]", "ae", txt)
                txt = re.sub("[öÖ]", "oe", txt)
                txt = re.sub("[üÜ]", "ue", txt)
                txt = re.sub("ß", "ss", txt)
                txt = re.sub(" ", "-", txt)
                txt = re.sub(pattern, "", txt)
                txt = txt.lower()
                url_dict[txt] = url
        except Exception as ex:
            return None
        return url_dict
