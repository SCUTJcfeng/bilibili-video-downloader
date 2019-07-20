# !/usr/bin/python3
# -*- coding:utf-8 -*-
'''
Author: jc feng
File Created: 2019-05-28 10:36:58
Last Modified: 2019-07-20 12:29:27
'''

from common.url import headers
from run import get_up_avs, get_video_by_aid, get_video_link, download_video


class TestAPi:

    test_up_id = 404427361
    test_av = 810872
    test_cid = 1176840

    def test_get_up_avs(self):
        assert len(get_up_avs(self.test_up_id)) >= 0

    def test_get_video_by_aid(self):
        video_data = get_video_by_aid(self.test_av)
        print(video_data)
        assert video_data.get('title') is not None
        assert video_data.get('owner') is not None
        pages = video_data.get('pages')
        assert isinstance(pages, list)
        for page in pages:
            assert page.get('cid') is not None
            assert page.get('part') is not None

    def test_get_video_link(self):
        video_link, sound_link = get_video_link(self.test_av, self.test_cid)
        print(video_link)
        print(sound_link)
        assert isinstance(video_link, list) and len(video_link) >= 1
        assert sound_link == '' or isinstance(sound_link, list)
        download_video(video_link[0], './test.mp4', headers)
