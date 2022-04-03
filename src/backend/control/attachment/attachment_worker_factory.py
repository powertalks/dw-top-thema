import datetime

from backend.control.attachment.attachment_worker_2008 import AttachmentWorker2008
from backend.control.attachment.attachment_worker_2016 import AttachmentWorker2016


class AttachmentWorkerFactory(object):

    def __init__(self):
        pass

    @classmethod
    def get_attachment_worker(cls, dt):
        if dt < datetime.date(2016, 7, 12):
            # Before 2016.07.12, extra web pages are downloaded for audio files.
            return AttachmentWorker2008()
        else:
            # After 2016.07.12, extra web pages are downloaded for manuscripts and exercises.
            return AttachmentWorker2016()
