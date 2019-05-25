# python 3.6

from common.http import HttpTool
# from werkzeug.utils import secure_filename
from common.save import SaveTool
from common.url import headers
from common.base import create_folder
from api import build_av_info_url, build_submit_av_list_url, build_video_dm_url, build_video_info_url
from config import AV_ID, UP_ID, BASE_DIR

# video_url = 'http://cn-zjwz-dx-v-03.acgvideo.com/upgcxcode/09/90/68089009/68089009-1-30080.m4s?expires=1558778400&platform=pc&ssig=bL_Fi9FiMWtl4fdRdOFKxg&oi=1901560625&nfa=uTIiNt+AQjcYULykM2EttA==&dynamic=1&trid=889e29e8bf5945d297dcd9b89c7722cd&nfb=maPYqpoel5MI3qOUX6YpRA==&nfc=1&mid=9854182'
# sound_url = 'https://cn-jxjj-dx-v-03.acgvideo.com/upgcxcode/16/56/93555616/93555616-1-30280.m4s'
# dm_url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=93555616'


def get_up_avs(mid):
    av_list = {}
    pass
    return av_list


def get_video_by_aid(aid):
    video_data = {}
    pass
    return video_data


def get_video_link(aid, cid):
    video_link = ''
    sound_link = ''
    pass
    return video_link, sound_link


def main():
    mid = UP_ID
    av_list = get_up_avs(mid)
    for av in av_list:
        author = av['author']
        aid = av['aid']
        video_data = get_video_by_aid(aid)
        title = video_data['title']
        for video in video_data['pages']:
            cid = video['cid']
            part = video['part']
            video_link, sound_link = get_video_link(aid, cid)
            create_folder([BASE_DIR, f'{mid}_{author}', f'{aid}_{title}'])
            video_name, sound_name = f'{cid}_{title}_{part}.mp4', f'{cid}_{title}_{part}.m4a'
            download_video(video_link, video_name, sound_link, sound_name)


def download_video(video_link, video_name, sound_link, sound_name):
    base_download(video_link, video_name, headers=headers)
    base_download(sound_link, sound_name, headers=headers)


def base_download(url, filename, headers=None):
    r = HttpTool.get(url, headers=headers, retFormat='raw')
    if not r:
        print(f'{filename} download fail')
        return False
    SaveTool.saveChunk(r, filename)
    print(f'{filename} download success')
    return True


if __name__ == '__main__':
    main()
