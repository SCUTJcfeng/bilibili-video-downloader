from util import RequestUtil, SaveTool, PathUtil, CONFIG, FFmpegUtil
from util.fs import legitimize
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
        self.title = ''
        self.owner = ''
        self.p_len = 0

    def print_vinfo(self):
        print('Owner:     ', self.owner)
        print('Title:     ', self.title)
        print('P_Num:     ', self.p_len)
        if self.p_len > 1:
            print('检测到多p视频，将下载全部视频')
        print()

    def print_pinfo(self, p_title, type_, quality):
        print('P_Title:   ', p_title)
        print('Type:      ', type_)
        print('Quality:   ', quality)
        print()

    def build_filename(self, p_title, i, ext, j=None):
        if self.p_len == 1:
            filename = f'{self.owner}-{self.title}（{p_title}）.{ext}'
        else:
            filename = f'{self.owner}-{self.title}（P{i}.{p_title}）.{ext}'
        if j is not None:
            filename = f'[{j}]-{filename}'
        return PathUtil.join_path(CONFIG['DOWNLOAD_PATH'], legitimize(filename))

    def run(self):
        video_list = self.get_video_info()
        self.print_vinfo()
        for i, video_info in enumerate(video_list):
            p_title, cid = video_info['part'], video_info['cid']
            download_data = self.get_sign_video_download_info(cid)
            self.print_pinfo(p_title, download_data['type'], BilibiliApi.QUALITY_EXT_MAP[download_data['quality']]['desc'])
            download_list = download_data['download_list']
            if download_data['type'] == 'durl':
                ext = BilibiliApi.QUALITY_EXT_MAP[download_data['quality']]['container']
                if len(download_list) == 1:
                    output = self.build_filename(p_title, i, ext)
                    self.download_video(download_list[0], output)
                    continue
                print('检测到多段视频')
                tmp_dl_list = []
                for j, url in enumerate(download_list):
                    tmp_video_name = self.build_filename(p_title, i, ext, j)
                    tmp_dl_list.append(tmp_video_name)
                    self.download_video(url, tmp_video_name)
                output = self.build_filename(p_title, i, 'mp4')
                self.merge_video(output, tmp_dl_list)
            else:
                ext = 'mp4'
                output = self.build_filename(p_title, i, ext)
                video_url, audio_url = download_list
                if not audio_url:
                    self.download_video(video_url, output)
                    continue
                tmp_video_name = self.build_filename(p_title, i, ext, 'video')
                self.download_video(video_url, tmp_video_name)
                tmp_audio_name = self.build_filename(p_title, i, ext, 'audio')
                self.download_video(audio_url, tmp_audio_name)
                tmp_dl_list = [tmp_video_name, tmp_audio_name]
                self.merge_video(output, tmp_dl_list)

    def merge_video(self, output, *files):
        if PathUtil.check_path(output):
            print(f'{output}已存在')
            return
        print('正在尝试合并视频，请参考控制台输出')
        FFmpegUtil(CONFIG['FFMPEG_PATH']).merge(*files, output=output)

    def get_video_info(self):
        request = BilibiliApi.build_aid_api_request(self.aid)
        response = RequestUtil.do_request(request)
        self.before_response(response)
        return self._decode_video_info(response.data)

    def _decode_video_info(self, video_info):
        video_list = []
        self.title, self.owner = video_info['title'], video_info['owner']['name']
        for page in video_info['pages']:
            cid, part = page['cid'], page['part']
            video_list.append({
                'part': part,
                'cid': cid,
            })
        self.p_len = len(video_list)
        return video_list

    def get_video_download_info(self, cid):
        request = BilibiliApi.build_cid_api_request(self.aid, cid)
        response = RequestUtil.do_request(request)
        self.before_response(response)
        return self._decode_video_download_info(response.data)

    def get_sign_video_download_info(self, cid):
        request = BilibiliApi.build_sign_cid_api_request(cid)
        response = RequestUtil.do_request(request)
        self.before_response(response)
        return self._decode_video_download_info(response.json)

    def _decode_video_download_info(self, download_info):
        download_data = {'quality': download_info['quality'], 'type': '', 'download_list': []}
        if 'durl' in download_info:
            download_data['type'] = 'durl'
            download_data['download_list'] = [d['url'] for d in download_info['durl']]
        elif 'dash' in download_info:
            dash = download_info['dash']
            download_data['type'] = 'dash'
            download_data['quality'] = dash['video'][0]['id']
            download_data['download_list'] = [dash['video'][0]['base_url'], dash['audio'][0]['base_url']]
        else:
            raise NotImplementedError
        return download_data

    def download_video(self, url, filename):
        if PathUtil.check_path(filename):
            print(f'{filename} exists, stop downloading')
            return
        retry_times = 2
        while retry_times > 0:
            try:
                request = BilibiliApi.build_video_download_request(url)
                response = RequestUtil.do_request(request, load_json=False, stream=True)
                self.before_response(response)
                self.save_video(response.raw_response, filename)
                break
            except:
                print(f'{filename} download fail, retry times = {retry_times}, restart...')
                retry_times -= 1
                if retry_times == 0:
                    raise Exception('retry times exceed, stop downloading...')
                continue

    def save_video(self, raw_response, filename):
        SaveTool.saveChunk(raw_response, filename)


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
