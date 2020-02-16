
from util import RequestUtil, SaveTool, PathUtil, secure_string, CONFIG
from api import BilibiliApi


class VideoDownload:
    def __init__(self, aid):
        self.aid = aid
        self.cid_list = []

    def build_filename(self, video_info, order, ext, video_format=None):
        owner, title, part = video_info['owner'], video_info['title'], video_info['part']
        filename = f'{owner}-{title}-{part}'
        if video_format:
            return secure_string(f'{filename}-{video_format}-{order}.{ext}')
        return secure_string(f'{filename}-{order}.{ext}')

    def run(self):
        video_list = self.get_video_info()
        for video_info in video_list:
            download_video_list = self.get_video_download_info(video_info['cid'])
            for download_data in download_video_list:
                for d_list in download_data['download_list']:
                    d_video, d_audio, d_order = d_list['video'], d_list['audio'], d_list['order']
                    video_name = self.build_filename(video_info, d_order, 'flv', download_data['video_format'])
                    self.download_video(d_video, video_name)
                    if d_audio:
                        audio_name = self.build_filename(video_info, d_order, 'mp3')
                        self.download_video(d_audio, audio_name)

    def before_response(self, response):
        if response.status_code != 200:
            print(response.raw_response.text)
            raise NotImplementedError
        if response.code is not None and response.code != 0:
            print(response.message)
            raise NotImplementedError
        return response

    def get_video_info(self):
        request = BilibiliApi.build_aid_api_request(self.aid)
        response = RequestUtil.do_request(request)
        self.before_response(response)
        return self._decode_video_info(response.data)

    def _decode_video_info(self, video_info):
        video_list = []
        title, owner = video_info['title'], video_info['owner']['name']
        for page in video_info['pages']:
            cid, part = page['cid'], page['part']
            video_list.append({
                'title': title,
                'owner': owner,
                'part': part,
                'cid': cid,
            })
        return video_list

    def get_video_download_info(self, cid):
        request = BilibiliApi.build_cid_api_request(self.aid, cid)
        response = RequestUtil.do_request(request)
        self.before_response(response)
        return self._decode_video_download_info(response.data)

    def _decode_video_download_info(self, download_info):
        download_list = []
        video_format, quality = download_info['format'], download_info['quality']
        if 'durl' in download_info:
            download_list.append({
                'type': 'durl',
                'video_format': video_format,
                'quality': quality,
                'download_list': [
                    {'video': d['url'], 'audio': None, 'order': d['order']} for d in download_info['durl']
                ],
            })
        elif 'dash' in download_info:
            dash = download_info['dash']
            download_list.append({
                'type': 'dash',
                'video_format': video_format,
                'quality': quality,
                'download_list': [{
                    'video': dash['video'][-1]['baseUrl'],
                    'audio': dash['audio'][1]['baseUrl'],
                    'order': 1
                }],
            })
        return download_list

    def download_video(self, url, filename):
        final_filename = PathUtil.join_path(CONFIG['ROOT_PATH'], filename)
        print(f'{final_filename} download start')
        print(f'download link: {url}')
        request = BilibiliApi.build_video_download_request(url)
        response = RequestUtil.do_request(request, load_json=False)
        self.before_response(response)
        self.save_video(response.raw_response, final_filename)

    def save_video(self, raw_response, filename):
        SaveTool.saveChunk(raw_response, filename)
        print(f'{filename} download success')


if __name__ == '__main__':
    for aid in CONFIG['AV_ID_LIST']:
        VideoDownload(aid).run()
