#!/usr/bin/python3
"""
1-top_ten
"""
try:
    import requests  # type: ignore
except Exception:
    # 'requests' is not available; provide a minimal fallback using urllib
    import urllib.request as _urllib_request
    import urllib.error as _urllib_error
    import json as _json

    class _SimpleResponse:
        def __init__(self, url, headers=None, allow_redirects=True):
            req = _urllib_request.Request(url, headers=headers or {})
            try:
                resp = _urllib_request.urlopen(req)
                self.status_code = resp.getcode()
                self._content = resp.read()
            except _urllib_error.HTTPError as e:
                self.status_code = e.code
                self._content = e.read()

        def json(self):
            try:
                return _json.loads(self._content.decode('utf-8'))
            except Exception:
                return {}

    class requests:
        RequestException = Exception

        @staticmethod
        def get(url, headers=None, allow_redirects=True):
            return _SimpleResponse(url, headers, allow_redirects)

#...existing code...
def top_ten(subreddit):
    """Prints the titles of the first 10 hot posts of a subreddit."""
    headers = {'User-Agent': 'Python:api_advanced:v1.0 (by /u/leam103)'}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code != 200:
            print(None)
            return

        data = response.json()
        posts = data.get('data', {}).get('children', [])
        for post in posts:
            print(post.get('data', {}).get('title'))

    except requests.RequestException:
        print(None)
       # ...existing code...
