
import os


class FFmpegUtil:
    def __init__(self, ffmpeg_path='ffmpeg'):
        self.ffmpeg = ffmpeg_path

    def merge(self, input_, *args, output):
        input_str = ' -i "' + input_ + '"'
        for arg in args:
            input_str += ' -i "' + arg + '"'
        os.system(f'{self.ffmpeg} {input_str} "{output}"')
