#!/usr/bin/python3
"""
2-recurse
"""
import importlib

try:
    requests = importlib.import_module('requests')
except Exception:
    # Fallback shim using urllib if 'requests' is not installed.
    import json
    from urllib import request as _urlrequest, parse as _parse

    class SimpleResponse:
        def __init__(self, status_code, data):
            self.status_code = status_code
            self._data = data

        def json(self):
            return self._data

    def _requests_get(url, headers=None, params=None, allow_redirects=False):
        if params:
            query = _parse.urlencode({k: v for k, v in params.items() if v is not None})
            url = url + ('?' + query if '?' not in url else '&' + query)
        req = _urlrequest.Request(url, headers=headers or {})
        try:
            with _urlrequest.urlopen(req) as resp:
                status = resp.getcode()
                raw = resp.read().decode('utf-8')
                data = json.loads(raw)
                return SimpleResponse(status, data)
        except Exception:
            return SimpleResponse(404, {})

    class _RequestsShim:
        @staticmethod
        def get(url, headers=None, params=None, allow_redirects=False):
            return _requests_get(url, headers=headers, params=params, allow_redirects=allow_redirects)

    requests = _RequestsShim()

def recurse(subreddit, hot_list=None, after=None):
    if hot_list is None:
        hot_list = []

    headers = {'User-Agent': 'python:alu-scripting:v1.0 (by /u/yourusername)'}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {'after': after, 'limit': 100}

    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)
        if response.status_code != 200:
            return None

        data = response.json().get('data', {})
        children = data.get('children', [])
        for child in children:
            hot_list.append(child['data']['title'])

        after = data.get('after')
        if after is None:
            return hot_list
        else:
            return recurse(subreddit, hot_list, after)
    except Exception:
        return None
