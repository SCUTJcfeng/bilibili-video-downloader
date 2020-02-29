
import os
import subprocess
from .file import PathUtil


class FFmpegUtil:
    def __init__(self, ffmpeg_path='ffmpeg'):
        self.ffmpeg = ffmpeg_path

    def merge(self, files, output):
        params = [self.ffmpeg]
        for f in files:
            params.extend(['-i', f])
        # params.extend(['-c', 'copy'])
        # params.extend(['-c:v', 'copy'])
        # params.extend(['-c:a', 'aac'])
        # params.extend(['-strict', 'experimental'])
        params.append(output)
        if PathUtil.check_path(output):
            os.remove(output)
        if subprocess.call(params, stdin=-3) == 0:
            print(f'merge into {output}')
            for part in files:
                os.remove(part)
