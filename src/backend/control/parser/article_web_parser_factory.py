import datetime

from backend.control.parser.arcitle_web_parser_2008 import ArticleWebParser2008
from backend.control.parser.article_web_parser_2016 import ArticleWebParser2016
from backend.control.parser.article_web_parser_2021 import ArticleWebParser2021
from backend.control.util.date_parser import DateParser
from backend.control.util.log_util import log_error
from backend.control.util.xml_util import get_html_root


class ArticleWebParserFactory(object):

    def __init__(self):
        pass

    @classmethod
    def get_article_web_parser(cls, file_path):
        # Parse date
        dt = ArticleWebParserFactory.parse_date_from_web_file(file_path)
        if dt is None:
            log_error("Failed to parse date from file \"{}\"!".format(file_path))
            return None
        return ArticleWebParserFactory.get_parser(dt)

    @classmethod
    def parse_date_from_web_file(cls, file_path):
        html_root = get_html_root(file_path)
        dt = ArticleWebParserFactory.try_parse_from_title(html_root)
        if dt is not None:
            return dt
        dt = ArticleWebParserFactory.try_parse_from_input_element(html_root)
        if dt is not None:
            return dt
        dt = ArticleWebParserFactory.try_parse_from_time_element(html_root)
        if dt is not None:
            return dt
        return None

    @classmethod
    def try_parse_from_title(cls, html_root):
        try:
            title_list = html_root.xpath("//title")
            if len(title_list) > 0:
                title = title_list[0]
                txt = title.text.strip()[-10:]
                return DateParser.try_parse_date(txt)
            else:
                log_error("No web title found in file \"{}\"!".format(html_root.base))
        except Exception as ex:
            log_error("Unexpected: failed to find the date in file \"{}\"! Reason: {}".format(html_root.base, str(ex)))
        return None

    @classmethod
    def try_parse_from_input_element(cls, html_root):
        try:
            input_list = html_root.xpath("//div[@class=\"mediaItem\"]/input[@name=\"display_date\"]")
            if len(input_list) > 0:
                input_elem = input_list[0]
                txt = input_elem.attrib["value"]
                return DateParser.try_parse_date(txt)
            else:
                return None
        except Exception as ex:
            log_error("Unexpected: failed to find the date in file \"{}\"! Reason: {}".format(html_root.base, str(ex)))
        return None

    @classmethod
    def try_parse_from_time_element(cls, html_root):
        try:
            elem_list = html_root.xpath("//time")
            if len(elem_list) > 0:
                txt = elem_list[0].text
                return DateParser.try_parse_date(txt)
            else:
                log_error("No \"time\" element in file \"{}\"!".format(html_root.base))
        except Exception as ex:
            log_error("Unexpected: failed to find the date in file \"{}\"! Reason: {}".format(html_root.base, str(ex)))
        return None

    @classmethod
    def get_parser(cls, dt):
        # The structure of the article web page was changed on two dates "2016.07.12" and "2021.01.01".
        if dt < datetime.date(2016, 7, 12):
            ps = ArticleWebParser2008()
        elif dt < datetime.date(2021, 1, 1):
            ps = ArticleWebParser2016()
        else:
            ps = ArticleWebParser2021()
        ps.date = dt
        return ps
