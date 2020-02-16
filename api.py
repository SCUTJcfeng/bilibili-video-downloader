
from util import Request, HttpMethod, CONFIG


class BilibiliApi:

    BASE_API_URL = 'https://api.bilibili.com'
    HEADERS = {
        'Origin': 'https://www.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Referer': 'https://www.bilibili.com'
    }

    @classmethod
    def build_oid_api_request(cls, mid, pn=1, ps=100, tid=0, order='pubdate', keyword=None):
        """
        返回 up 所有的视频av 号
        :param mid: up id
        :param pn:
        :param ps: 每页数量
        :param tid: 0：全部
        :param order:
        :param keyword:
        :return:
        """
        url = cls.BASE_API_URL + '/x/space/arc/search'
        params = {
            'mid': mid,
            'pn': pn,
            'ps': ps,
            'tid': tid,
            'order': order,
            'keyword': keyword,
        }
        return Request(url=url, method=HttpMethod.GET, params=params, headers=cls.HEADERS)

    @classmethod
    def build_aid_api_request(cls, aid):
        """
        根据 aid 获取视频信息
        :param aid:
        :return:
        """
        url = cls.BASE_API_URL + '/x/web-interface/view'
        params = {
            'aid': aid
        }
        return Request(url=url, method=HttpMethod.GET, params=params, headers=cls.HEADERS)

    @classmethod
    def build_cid_api_request(cls, avid, cid):
        """
        获取视频下载信息
        :param avid:
        :param cid:
        :return:
        """
        url = cls.BASE_API_URL + '/x/player/playurl'
        params = {
            'avid': avid,
            'cid': cid,
            'qn': 80,
            'fnver': 0,
            'fnval': 16,
        }
        cookies = {
            'SESSDATA': CONFIG['SESSION_DATA']
        }
        return Request(url=url, method=HttpMethod.GET, params=params, headers=cls.HEADERS, cookies=cookies)

    @classmethod
    def build_archive_api_request(cls, aid):
        """
        获取视频统计信息，包含合集
        :param aid:
        :return:
        """
        url = cls.BASE_API_URL + '/x/web-interface/archive/stat'
        params = {
            'aid': aid
        }
        return Request(url=url, method=HttpMethod.GET, params=params, headers=cls.HEADERS)

    @classmethod
    def build_dm_api_request(cls, oid):
        """
        获取弹幕信息
        :param oid:
        :return:
        """
        url = cls.BASE_API_URL + '/x/v1/dm/list.so'
        params = {
            'oid': oid,
        }
        return Request(url=url, method=HttpMethod.GET, params=params, headers=cls.HEADERS)

    @classmethod
    def build_video_download_request(cls, url):
        """
        下载视频
        :param url:
        :return:
        """
        return Request(url=url, method=HttpMethod.GET, headers=cls.HEADERS)
