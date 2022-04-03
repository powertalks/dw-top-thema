import datetime

from main.global_vars import g_date_format


# This class keeps the information about the URLs of the learning material, i.e. URLs to the manuscripts, exercises,
# audio files and their local path.
class ArticleInfo(object):

    def __init__(self):
        self.file_path = ""
        self.date = None
        self.manuscript_pdf_url = ""
        self.exercise_pdf_url = ""
        self.audio_url = ""
        self.manuscript_file_path = ""
        self.exercise_file_path = ""
        self.audio_file_path = ""

    def to_dict(self):
        txt_dict = dict()
        txt_dict["file_path"] = self.file_path
        txt_dict["date"] = self.date.strftime(g_date_format)
        txt_dict["manuscript_pdf_url"] = self.manuscript_pdf_url
        txt_dict["exercise_pdf_url"] = self.exercise_pdf_url
        txt_dict["audio_url"] = self.audio_url
        txt_dict["manuscript_file_path"] = self.manuscript_file_path
        txt_dict["exercise_file_path"] = self.exercise_file_path
        txt_dict["audio_file_path"] = self.audio_file_path
        return txt_dict

    @classmethod
    def from_dict(self, dict_obj):
        info = ArticleInfo()
        info.file_path = dict_obj["file_path"]
        info.date = datetime.datetime.strptime(dict_obj["date"], g_date_format).date()
        info.manuscript_pdf_url = dict_obj["manuscript_pdf_url"]
        info.exercise_pdf_url = dict_obj["exercise_pdf_url"]
        info.audio_url = dict_obj["audio_url"]

        if "manuscript_file_path" in dict_obj:
            info.manuscript_file_path = dict_obj["manuscript_file_path"]

        if "exercise_file_path" in dict_obj:
            info.exercise_file_path = dict_obj["exercise_file_path"]

        if "audio_file_path" in dict_obj:
            info.audio_file_path = dict_obj["audio_file_path"]
        return info
