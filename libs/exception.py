from config import TIMOUT

class VideoException(Exception):
    def __init__(self):
        super(VideoException, self).__init__()
        self.message = "Some basic exception"


class VideoIsTooLongException(VideoException):
    def __init__(self):
        super(VideoIsTooLongException, self).__init__()
        self.message = "😲 The video is too long. It should be no more than 2 minutes and contain no more than 4k frames."


class VideoIsTooBigException(VideoException):
    def __init__(self):
        super(VideoIsTooBigException, self).__init__()
        self.message = "😮 The video is too big. It should not be more than 2000 by 2000 px."


class MoreThanOneVideoException(VideoException):
    def __init__(self):
        super(MoreThanOneVideoException, self).__init__()
        self.message = f"☝️ You cannot submit more than one video in {TIMOUT} seconds. Please wait and try again."
