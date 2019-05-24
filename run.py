import requests

sound_url = 'https://cn-jxjj-dx-v-03.acgvideo.com/upgcxcode/16/56/93555616/93555616-1-30280.m4s?expires=1558730700&platform=pc&ssig=49SEiXa3jXJ-mncm-SH7Cw&oi=2004568188&trid=8dd55c83f4cc4b7bbead427bc698211b&nfb=maPYqpoel5MI3qOUX6YpRA==&nfc=1'
video_url = 'https://cn-jxjj-dx-v-03.acgvideo.com/upgcxcode/16/56/93555616/93555616-1-30080.m4s?expires=1558730400&platform=pc&ssig=ShAuuRKyqj92PDlvtuBLUg&oi=2004568188&trid=28d5948c56624a6aa316daf11f04f33f&nfb=maPYqpoel5MI3qOUX6YpRA==&nfc=1'
dm_url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=93555616'
img_url = 'https://errorpage.b0.upaiyun.com/sfault-image-404'

headers = {
    'Host': 'cn-jxjj-dx-v-03.acgvideo.com',
    'Connection': 'keep-alive',
    'Origin': 'https://www.bilibili.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'DNT': '1',
    'Accept': '*/*',
    'Referer': 'https://www.bilibili.com/video/av53476879',
    'Accept-Encoding': 'identity',
    'Range': 'bytes=0-',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,la;q=0.7',
    'If-Range': '0-'
}


def base_download(url, filename, headers=None):
    session = requests.Session()
    flag = False
    with session.get(url, headers=headers) as r:
        r.raise_for_status()
        with open(filename, 'wb+') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    if not flag:
                        flag = True
    return flag


def download_video():
    res = base_download(url=video_url, filename='./temp_video.mp4', headers=headers)
    res = base_download(url=sound_url, filename='./temp_sound.mp4', headers=headers)
    print(f'video download {res}')



def download_dm():
    pass


def download_img():
    res = base_download(url=img_url, filename='./temp.png')
    print(f'img download {res}')


if __name__ == '__main__':
    download_video()
    # download_img()
