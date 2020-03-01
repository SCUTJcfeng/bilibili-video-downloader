
import os
import subprocess
from .file import PathUtil


def get_usable_ffmpeg(cmd='ffmpeg'):
    try:
        p = subprocess.Popen([cmd, '-version'], stdin=-3, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        vers = str(out, 'utf-8').split('\n')[0].split()
        assert (vers[0] == 'ffmpeg' and vers[2][0] > '0') or (vers[0] == 'avconv')
        try:
            v = vers[2][1:] if vers[2][0] == 'n' else vers[2]
            version = [int(i) for i in v.split('.')]
        except:
            version = [1, 0]
        return cmd, version
    except:
        print(f'{cmd} 不存在')
        return None, None


FFMPEG, VERSION = get_usable_ffmpeg()


class FFmpegUtil:
    def __init__(self, ffmpeg_path):
        self.ffmpeg = ffmpeg_path or FFMPEG

    def merge(self, files, output):
        params = [self.ffmpeg]
        for f in files:
            params.extend(['-i', f])
        params.extend(['-loglevel', 'quiet'])
        params.extend(['-c', 'copy'])
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
