# python 3.6


_SUBMIT_VIDEOS_BASE_URL = 'https://space.bilibili.com/ajax/member/getSubmitVideos'
_AV_INFO_URL = 'https://api.bilibili.com/x/web-interface/view'
_VIDEO_INFO_URL = 'https://api.bilibili.com/x/player/playurl'
_VIDEO_DM_URL = 'https://api.bilibili.com/x/v1/dm/list.so'


def build_submit_videos_url(mid, page):
    return _SUBMIT_VIDEOS_BASE_URL + '?mid={0}&pagesize=100&tid=0&page={1}&keyword=&order=pubdate'.format(mid, page)


def build_av_info_url(aid):
    return _AV_INFO_URL + '?aid={0}'.format(aid)


def build_video_info_url(aid, cid):
    return _VIDEO_INFO_URL + '?avid={0}&cid={1}&qn=80&type=&fnver=0&fnval=16&otype=json'.format(aid, cid)


def build_video_dm_url(aid):
    return _VIDEO_DM_URL + '?oid={0}'.format(aid)
