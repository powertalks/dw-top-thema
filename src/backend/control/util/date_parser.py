import datetime


class DateParser(object):

    def __init__(self):
        pass

    @classmethod
    def try_parse_date(cls, txt):
        dt = DateParser.try_parse_with_format(txt, "%d.%m.%Y")
        if dt is not None:
            return dt

        dt = DateParser.try_parse_with_format(txt, "%Y%m%d")
        if dt is not None:
            return dt

        return None

    @classmethod
    def try_parse_with_format(cls, txt, fmt):
        try:
            dt = datetime.datetime.strptime(txt, fmt)
            return dt.date()
        except ValueError as ex:
            return None
