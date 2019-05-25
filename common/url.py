# python3.6


class UrlTool:
    @staticmethod
    def joinUrl(url, params):
        return url + '?' + '&'.join([f'{k}={v}' for k, v in params.items()])


headers = {
    'Origin': 'https://www.bilibili.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Referer': 'https://www.bilibili.com'
}
