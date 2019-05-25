# python3.6

import traceback
import requests
import urllib3
urllib3.disable_warnings()


class HttpTool:
    @staticmethod
    def get(url, params=None, headers=None, retFormat='text', timeout=10):
        res = None
        try:
            res = requests.get(url, params=params, headers=headers, timeout=timeout)
        except:
            traceback.print_exc()
        return HttpTool.beforeReturn(res, retFormat)

    @staticmethod
    def post(url, data=None, json=None, headers=None, retFormat='text', timeout=10, verify=True):
        res = None
        try:
            res = requests.post(url, data=data, json=json, headers=headers, timeout=timeout, verify=verify)
        except:
            traceback.print_exc()
        return HttpTool.beforeReturn(res, retFormat)

    @staticmethod
    def beforeReturn(res, retFormat):
        assert retFormat == 'text' or retFormat == 'json' or 'raw'
        if retFormat == 'text':
            return res.text if isinstance(res, requests.Response) else ''
        elif retFormat == 'json':
            return res.json() if isinstance(res, requests.Response) else {}
        else:
            return res
