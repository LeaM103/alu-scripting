#!/usr/bin/python3
"""Get the titles of the first 10 hot posts for a given subreddit."""
import requests


def top_ten(subreddit):
    headers = {"User-Agent": "Python:top_ten:v1.0 (by /u/yourusername)"}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)

        # If subreddit does not exist or redirects
        if response.status_code != 200:
            print(None)
            return

        posts = response.json().get("data", {}).get("children", [])

        for post in posts:
            print(post.get("data", {}).get("title"))

    except Exception:
        print(None)

