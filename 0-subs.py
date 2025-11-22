#!/usr/bin/python3
"""
0-subs
"""
import importlib

try:
    requests = importlib.import_module("requests")
except Exception:
    # Fallback to urllib if requests isn't installed
    import urllib.request
    import urllib.error
    import json

    class _SimpleResponse:
        def __init__(self, code, content):
            self.status_code = code
            self._content = content

        def json(self):
            return json.loads(self._content.decode('utf-8') if isinstance(self._content, (bytes, bytearray)) else self._content)

    def _requests_get(url, headers=None, allow_redirects=True):
        req = urllib.request.Request(url, headers=headers or {})
        try:
            with urllib.request.urlopen(req) as resp:
                code = resp.getcode()
                content = resp.read()
                return _SimpleResponse(code, content)
        except urllib.error.HTTPError as e:
            content = e.read() if hasattr(e, 'read') else b''
            return _SimpleResponse(e.code if hasattr(e, 'code') else 0, content)
        except Exception:
            return _SimpleResponse(0, b'')

    # expose a requests-like interface
    class requests:
        @staticmethod
        def get(url, headers=None, allow_redirects=True):
            return _requests_get(url, headers=headers, allow_redirects=allow_redirects)


def number_of_subscribers(subreddit):
    """Return the total number of subscribers for a subreddit."""
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = {"User-Agent": "ubuntu:0-subs:v1.0 (by /u/yourusername)"}

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code != 200:
            return 0

        data = response.json()
        return data.get("data", {}).get("subscribers", 0)
    except Exception:
        return 0
