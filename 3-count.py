#!/usr/bin/python3
"""
3-count.py
"""
try:
    import importlib
    requests = importlib.import_module('requests')
except Exception:
    import urllib.request
    import urllib.parse
    import urllib.error
    import json

    class SimpleResponse:
        def __init__(self, code, content):
            self.status_code = code
            self._content = content

        def json(self):
            return json.loads(self._content.decode('utf-8'))

    def requests_get(url, headers=None, params=None, allow_redirects=False):
        if params:
            q = urllib.parse.urlencode(params)
            url = url + ('?' if '?' not in url else '&') + q
        req = urllib.request.Request(url, headers=headers or {})
        try:
            with urllib.request.urlopen(req) as resp:
                content = resp.read()
                return SimpleResponse(resp.getcode(), content)
        except urllib.error.HTTPError as e:
            return SimpleResponse(e.code, e.read())

    class _RequestsFallback:
        pass

    requests = _RequestsFallback()
    requests.get = requests_get


def count_words(subreddit, word_list, hot_list=[], counts=None, after=None):
    """Recursively queries Reddit API, counts keywords in hot post titles, and prints sorted results."""
    
    if counts is None:
        counts = {}

    headers = {'User-Agent': 'Python:3-count:v1.0 (by /u/yourusername)'}
    url = f'https://www.reddit.com/r/{subreddit}/hot.json'
    params = {'limit': 100, 'after': after}
    
    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)
        if response.status_code != 200:
            return
        data = response.json()
        posts = data.get('data', {}).get('children', [])
        if not posts:
            return
        for post in posts:
            title = post.get('data', {}).get('title', '')
            # Split title into words, lowercase
            words_in_title = title.lower().split()
            for keyword in word_list:
                keyword_lower = keyword.lower()
                count = words_in_title.count(keyword_lower)
                if count:
                    counts[keyword_lower] = counts.get(keyword_lower, 0) + count
        # Recursive call for next page
        after = data.get('data', {}).get('after', None)
        if after:
            return count_words(subreddit, word_list, hot_list, counts, after)
        # Print results sorted by count desc, then alphabetically
        sorted_counts = sorted(
            [(k, v) for k, v in counts.items() if v > 0],
            key=lambda x: (-x[1], x[0])
        )
        for k, v in sorted_counts:
            print(f"{k}: {v}")
    except Exception:
        return
