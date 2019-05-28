# python 3.6

from common.url import headers
from run import get_up_avs, get_video_by_aid, get_video_link, secure_string, download_video
from common.base import create_folder, create_path, check_path
from config import BASE_DIR


test_up_id = None
test_av_list = [810872]


def test():
    av_list = get_up_avs(test_up_id)
    av_list.extend(test_av_list)
    for aid in av_list:
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


if __name__ == "__main__":
    test()
