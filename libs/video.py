import os
from pathlib import Path
from shutil import copyfile
from uuid import uuid1

import ffmpeg

from config import TEMP
from libs.exception import VideoIsTooLongException, VideoIsTooBigException

temp = Path(TEMP)
lib = Path("./libs")


class Video:
    def __init__(self, bot, video, w_out=768, h_out=480, r=0.15):
        self.video = video
        self.file_name = str(uuid1()) + "." + video.mime_type.split("/")[1]
        self.full_file_name = str(temp / self.file_name)
        self.full_wide_file_name = str(temp / ("wide_" + self.file_name))
        self.bot = bot
        self.w_out = w_out
        self.h_out = h_out
        self.r = r

        self.check_size()

        self.file_url = bot.get_file_url(video.file_id)
        copyfile(lib / 'song.mp3', temp / (self.file_name + ".mp3"))
        self.song_name = str(temp / (self.file_name + ".mp3"))

    def make_wide(self):
        stream = ffmpeg.input(self.file_url)
        stream = ffmpeg.filter(stream.video, "scale", -1, self.h_out)
        stream = ffmpeg.crop(stream, f"iw / 2 - {self.w_out * self.r / 2}", "0", f"{self.w_out * self.r}", "ih")
        stream = ffmpeg.filter(stream, "scale", 768, 480)
        stream = ffmpeg.filter(stream, "setsar", 1)
        audio = ffmpeg.input(self.song_name)

        out = ffmpeg.output(stream, audio, self.full_wide_file_name, shortest=None, y=None)
        out.run()

        return self.full_wide_file_name

    def remove_files(self):
        if os.path.exists(self.song_name):
            os.remove(self.song_name)
        if os.path.exists(self.full_wide_file_name):
            os.remove(self.full_wide_file_name)

    def check_size(self):
        try:
            if self.video.duration and self.video.duration > 120:
                raise VideoIsTooLongException()
        except:
            pass
        try:
            if self.video.width and self.video.width > 2000 or self.video.height and self.video.height > 2000:
                raise VideoIsTooBigException()
        except:
            pass
