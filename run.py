
from util import RequestUtil, SaveTool, PathUtil, secure_string, CONFIG, FFmpegUtil
from api import BilibiliApi


class Base:
    def before_response(self, response):
        if response.status_code != 200:
            print(response.raw_response.text)
            raise NotImplementedError
        if response.code is not None and response.code != 0:
            print(response.message)
            raise NotImplementedError
        return response


class VideoDownload(Base):
    def __init__(self, aid):
        self.aid = aid

    def build_filename(self, video_info, quality, order, ext):
        owner, title, part = video_info['owner'], video_info['title'], video_info['part']
        if order:
            return secure_string(f'{owner}-{title}-{part}-{quality}-{order}.{ext}')
        return secure_string(f'{owner}-{title}-{part}-{quality}.{ext}')

    def run(self):
        video_list = self.get_video_info()
        for video_info in video_list:
            download_video_list = self.get_video_download_info(video_info['cid'])
            video_name_list, audio_name_list = [], []
            for download_data in download_video_list:
                for d_list in download_data['download_list']:
                    d_video, d_audio, d_order = d_list['video'], d_list['audio'], d_list['order']
                    video_name = self.build_filename(
                        video_info, download_data['quality'], d_order, download_data['video_format'])
                    video_name = self.download_video(d_video, video_name)
                    video_name_list.append(video_name)
                    if d_audio:
                        audio_name = self.build_filename(video_info, download_data['quality'], d_order, 'mp3')
                        audio_name = self.download_video(d_audio, audio_name)
                        audio_name_list.append(audio_name)
            if CONFIG['AUTO_MERGE']:
                output_video, output_audio = video_name_list[0], audio_name_list[0]
                if len(video_name_list) > 1:
                    output_video = self.merge_video(video_name_list[0], video_name_list[1:])
                if len(audio_name_list) > 1:
                    output_audio = self.merge_video(audio_name_list[0], audio_name_list[1:])
                self.merge_video(output_video, output_audio)

    def merge_video(self, video, *args):
        tmp_list = video.split('/')
        tmp_list[-1] = 'merge-' + tmp_list[-1]
        output = '/'.join(tmp_list)
        if PathUtil.check_path(output):
            print(f'{output}已存在')
            return output
        print('正在尝试合并视频，请参考控制台输出')
        FFmpegUtil(CONFIG['FFMPEG_PATH']).merge(video, *args, output=output)
        return output

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
        quality = download_info['quality']
        if 'durl' in download_info:
            download_list.append({
                'type': 'durl',
                'video_format': 'flv',
                'quality': quality,
                'download_list': [
                    {'video': d['url'], 'audio': None, 'order': d['order']} for d in download_info['durl']
                ],
            })
        elif 'dash' in download_info:
            dash = download_info['dash']
            download_list.append({
                'type': 'dash',
                'video_format': 'mp4',
                'quality': quality,
                'download_list': [{
                    'video': dash['video'][0]['base_url'],
                    'audio': dash['audio'][0]['base_url'],
                    'order': None
                }],
            })
        return download_list

    def download_video(self, url, filename):
        final_filename = PathUtil.join_path(CONFIG['DOWNLOAD_PATH'], filename)
        if PathUtil.check_path(final_filename):
            print(f'{final_filename} exists, stop downloading')
            return final_filename
        print(f'{filename} download start')
        request = BilibiliApi.build_video_download_request(url)
        response = RequestUtil.do_request(request, load_json=False)
        self.before_response(response)
        self.save_video(response.raw_response, final_filename)
        return final_filename

    def save_video(self, raw_response, filename):
        SaveTool.saveChunk(raw_response, filename)
        print(f'{filename} download success')


class VideoSearch(Base):
    def __init__(self, up_id, order, keyword):
        self.up_id = up_id
        self.order = order
        self.keyword = keyword

    def get_aid_list(self):
        if not all([self.up_id, self.order, self.keyword]):
            print('UP_ID, ORDER, KEYWORD 信息不全，筛选退出')
            return []
        aid_list, page = [], 1
        while True:
            vlist = self.get_oid_info_by_page(page)
            if not vlist:
                break
            aid_list.extend(vlist)
            page += 1
        print(f'按up：{self.up_id} 关键词：{self.keyword} 共找到{len(aid_list)}条相关视频')
        return aid_list

    def get_oid_info_by_page(self, page):
        request = BilibiliApi.build_oid_api_request(self.up_id, page, order=self.order, keyword=self.keyword)
        response = RequestUtil.do_request(request)
        self.before_response(response)
        return self._decode_oid_info(response.data)

    def _decode_oid_info(self, data):
        return [v['aid'] for v in data['list']['vlist']]


if __name__ == '__main__':
    for aid in VideoSearch(CONFIG['UP_ID'], CONFIG['ORDER'], CONFIG['KEYWORD']).get_aid_list():
        VideoDownload(aid).run()
    for aid in CONFIG['AV_ID_LIST']:
        VideoDownload(aid).run()
