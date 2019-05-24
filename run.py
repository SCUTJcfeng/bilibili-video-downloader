import requests

url = 'https://cn-jxjj-dx-v-03.acgvideo.com/upgcxcode/16/56/93555616/93555616-1-30280.m4s?expires=1558727700&platform=pc&ssig=A8V3jrho790D9U0IDOGEBw&oi=2004568188&trid=2f2f9aa00e1e4249847435155ff28201&nfb=maPYqpoel5MI3qOUX6YpRA==&nfc=1'
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
    'Rangee': 'bytes=3095606-3183466',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,la;q=0.7',
    'If-Range': '5ce80e54-8fc6d3'
}


def base_download(url, filename, headers=None):
    session = requests.Session()
    flag = False
    with session.get(url, headers=headers) as r:
        r.raise_for_status()
        with open(filename, 'wb+') as f:
            for chunk in r.iter_content():
                if chunk:
                    f.write(chunk)
                    if not flag:
                        flag = True
    return flag


def download_video():
    res = base_download(url=url, filename='./temp.mp4', headers=headers)
    print(f'video download {res}')


def download_img():
    res = base_download(url=img_url, filename='./temp.png')
    print(f'img download {res}')



if __name__ == '__main__':
    # download_video()
    download_img()
