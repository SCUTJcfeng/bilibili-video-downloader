
import json
from requests import sessions


class HttpMethod:
    GET = 'get'
    POST = 'post'
    DELETE = 'delete'


class RequestUtil:
    session = sessions.Session()

    @classmethod
    def do_request(cls, request, load_json=True, stream=False):
        response = cls.session.request(
            method=request.method,
            url=request.url,
            headers=request.headers,
            params=request.params,
            cookies=request.cookies,
            stream=stream,
            timeout=10)
        return cls.build_response(request, response, load_json)

    @classmethod
    def build_response(cls, request, raw_response, load_json):
        return Response(request=request, raw_response=raw_response, load_json=load_json)


class Request:
    def __init__(self, url, method=HttpMethod.GET, params=None, data=None, headers=None, cookies=None):
        self._url = url
        self._method = method
        self._params = params
        self._data = data
        self._headers = headers
        self._cookies = cookies

    @property
    def url(self):
        return self._url

    @property
    def method(self):
        return self._method

    @property
    def params(self):
        return self._params

    @property
    def data(self):
        return self._data

    @property
    def headers(self):
        return self._headers

    @property
    def cookies(self):
        return self._cookies


class Response:
    def __init__(self, request, raw_response, load_json=True):
        self._request = request
        self._raw_response = raw_response
        self._json_data = json.loads(self._raw_response.text) if load_json else {}

    @property
    def request(self):
        return self._request

    @property
    def raw_response(self):
        return self._raw_response

    @property
    def status_code(self):
        return self._raw_response.status_code

    @property
    def json(self):
        return self._json_data

    @property
    def code(self):
        return self._json_data.get('code', None)

    @property
    def data(self):
        return self._json_data.get('data', None)

    @property
    def message(self):
        return self._json_data.get('message', None)
