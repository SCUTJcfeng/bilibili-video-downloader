# python 3.6

from common.http import HttpTool
from common.save import SaveTool
from common.url import headers

video_url = 'http://cn-zjwz-dx-v-03.acgvideo.com/upgcxcode/09/90/68089009/68089009-1-30080.m4s?expires=1558778400&platform=pc&ssig=bL_Fi9FiMWtl4fdRdOFKxg&oi=1901560625&nfa=uTIiNt+AQjcYULykM2EttA==&dynamic=1&trid=889e29e8bf5945d297dcd9b89c7722cd&nfb=maPYqpoel5MI3qOUX6YpRA==&nfc=1&mid=9854182'
sound_url = 'https://cn-jxjj-dx-v-03.acgvideo.com/upgcxcode/16/56/93555616/93555616-1-30280.m4s'
dm_url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=93555616'
img_url = 'https://errorpage.b0.upaiyun.com/sfault-image-404'

video_info_url = 'https://api.bilibili.com/x/web-interface/view?aid=5347687'


def base_download(url, filename, headers=None, data=None, params=None):
    r = HttpTool.get(url, params, headers=headers, retFormat='raw')
    if not r:
        return False
    SaveTool.saveChunk(r, filename)
    return True


def download_video():
    # res = base_download(url=sound_url, filename='./temp_sound.mp4', headers=headers)
    res = base_download(url=video_url, filename='./temp_video.mp4', headers=headers)
    print(f'video download {res}')


def download_dm():
    res = base_download(url=dm_url, filename='./dm.xml')
    print(f'dm download {res}')


def download_img():
    res = base_download(url=img_url, filename='./temp.png')
    print(f'img download {res}')


if __name__ == '__main__':
    # download_dm()
    download_video()
    # download_img()
