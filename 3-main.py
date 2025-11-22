#!/usr/bin/python3
"""
3-main.py
"""
import sys

if __name__ == '__main__':
    count_words = __import__('3-count').count_words
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        # Pass subreddit and list of keywords to count_words
        count_words(sys.argv[1], [x for x in sys.argv[2].split()])
