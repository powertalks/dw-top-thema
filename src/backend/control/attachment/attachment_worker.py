from main.global_vars import is_manuscript_selected, is_exercise_selected, is_audio_selected


# Base class for attachment downloading.
class AttachmentWorker(object):

    def __init__(self):
        self.output_dir = ""
        self.cache_dir = ""
        self.article_info = None

    def fetch_attachments(self):
        result = True

        if is_manuscript_selected():
            if not self.fetch_manuscript():
                result = False

        if is_exercise_selected():
            if not self.fetch_exercise():
                result = False

        if is_audio_selected():
            if not self.fetch_audio():
                result = False
        return result

    def fetch_manuscript(self):
        # This is a virtual function.
        raise NotImplementedError()

    def fetch_exercise(self):
        # This is a virtual function.
        raise NotImplementedError()

    def fetch_audio(self):
        # This is a virtual function.
        raise NotImplementedError()
