
import pytest
from api import BilibiliApi
from util import RequestUtil
from run import VideoDownload


class TestAPi:
    """
    测试 Bilibili api 接口
    """

    test_up_id = 404427361
    test_av = 810872
    test_cid = 1176840

    @staticmethod
    def do_request_and_check_response(request):
        response = RequestUtil.do_request(request)
        assert response.status_code == 200
        assert response.code == 0
        assert isinstance(response.data, dict)
        return response.data

    @pytest.mark.api
    @pytest.mark.parametrize('oid', [
        14110780,
        404427361
    ])
    def test_bilibili_oid_api(self, oid):
        request = BilibiliApi.build_oid_api_request(oid)
        data = self.do_request_and_check_response(request)
        assert 'list' in data
        assert 'vlist' in data['list']

    @pytest.mark.api
    @pytest.mark.parametrize('aid', [
        810872,
        4159781
    ])
    def test_bilibili_aid_api(self, aid):
        request = BilibiliApi.build_aid_api_request(aid)
        data = self.do_request_and_check_response(request)
        assert 'title' in data
        assert 'owner' in data
        assert 'pages' in data
        assert isinstance(data['pages'], list)

    @pytest.mark.api
    @pytest.mark.parametrize('aid, cid', [
        (810872, 1176840),
        (4159781, 6718181)
    ])
    def test_bilibili_cid_api(self, aid, cid):
        request = BilibiliApi.build_cid_api_request(aid, cid)
        data = self.do_request_and_check_response(request)
        assert 'quality' in data
        assert 'format' in data
        if 'durl' in data:
            assert isinstance(data['durl'], list)
        elif 'dash' in data:
            assert isinstance(data['dash'], dict)
        else:
            assert False

    @pytest.mark.api
    @pytest.mark.parametrize('aid', [
        810872,
        4159781
    ])
    def test_bilibili_archive_api(self, aid):
        request = BilibiliApi.build_archive_api_request(aid)
        data = self.do_request_and_check_response(request)
        assert 'view' in data
        assert 'danmaku' in data
        assert 'reply' in data
        assert 'favorite' in data
        assert 'coin' in data
        assert 'share' in data
        assert 'like' in data
        assert 'now_rank' in data
        assert 'his_rank' in data

    @pytest.mark.api
    @pytest.mark.parametrize('cid', [
        1176840,
        6718181
    ])
    def test_bilibili_archive_api(self, cid):
        request = BilibiliApi.build_dm_api_request(cid)
        response = RequestUtil.do_request(request, load_json=False)
        assert response.status_code == 200

    @pytest.mark.api
    @pytest.mark.parametrize('aid, cid', [
        (810872, 1176840),
        (4159781, 6718181)
    ])
    def test_bilibili_download_api(self, aid, cid):
        instance = VideoDownload(aid)
        download_video_list = instance.get_video_download_info(cid)
        download_data = download_video_list[0]['download_list'][0]
        video, audio = download_data['video'], download_data['audio']
        assert video
