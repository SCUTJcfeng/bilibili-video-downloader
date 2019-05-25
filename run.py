# python 3.6

from common.http import HttpTool
from common.save import SaveTool
from common.url import headers
from common.base import create_folder, create_path, check_path
from api import build_av_info_url, build_submit_videos_url, build_video_info_url
from config import AV_ID, UP_ID, BASE_DIR


def get_up_avs(mid):
    av_list = []
    if not mid:
        return av_list
    page = 0
    while True:
        page += 1
        av_url = build_submit_videos_url(mid, page)
        res = HttpTool.get(av_url, retFormat='json')
        if not res:
            break
        data = res['data']
        av_list.extend(data['vlist'])
        if data['pages'] == page:
            break
    return av_list


def get_video_by_aid(aid):
    video_data = {}
    url = build_av_info_url(aid)
    res = HttpTool.get(url, retFormat='json')
    if res and res['code'] == 0:
        video_data = res['data']
    return video_data


def get_video_link(aid, cid):
    video_link = ''
    sound_link = ''
    url = build_video_info_url(aid, cid)
    res = HttpTool.get(url, retFormat='json')
    if res and res['code'] == 0:
        data = res['data']
        if 'dash' in data:
            dash = data['dash']
            video_link = dash['video'][-1]['baseUrl']
            sound_link = dash['audio'][1]['baseUrl']
        elif 'durl' in data:
            video_link = data['durl'][0]['url']
    return video_link, sound_link


def secure_string(string):
    string = string.replace('！', '!').replace('\\', '_').replace('/', '_')
    string = string.replace('？', '_').replace('<', '_').replace('>', '_')
    string = string.replace('<', '_').replace('|', '1').replace('*', '.')
    string = string.replace(':', '.').replace('"', '\'').strip()
    return string


def main():
    av_list = get_up_avs(UP_ID)
    av_list.extend(AV_ID)
    for av in av_list:
        aid = av['aid'] if isinstance(av, dict) else av
        video_data = get_video_by_aid(aid)
        title = secure_string(video_data['title'])
        owner = video_data['owner']
        for video in video_data['pages']:
            cid = video['cid']
            part = video['part']
            video_link, sound_link = get_video_link(aid, cid)
            path = create_folder(BASE_DIR, f'{owner["mid"]}_{secure_string(owner["name"])}', f'{aid}_{title}')
            video_name, sound_name = create_path(path, f'{cid}_{title}_{part}.mp4'), create_path(path, f'{cid}_{title}_{part}.m4a')
            if not video_link or check_path(video_name):
                print(f'{video_name} already exists or link is null')
            else:
                download_video(video_link, video_name, headers=headers)
            if not sound_link or check_path(sound_name):
                print(f'{sound_name} already exists or link is null')
            else:
                download_video(sound_link, sound_name, headers=headers)


def download_video(url, filename, headers=None):
    r = HttpTool.get(url, headers=headers, retFormat='raw')
    if not r:
        print(f'{filename} download fail')
        return False
    SaveTool.saveChunk(r, filename)
    print(f'{filename} download success')
    return True


if __name__ == '__main__':
    main()
