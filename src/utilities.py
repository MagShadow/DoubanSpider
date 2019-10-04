import re
import time
import numpy as np
from bs4 import BeautifulSoup

headers_ua = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}]
headers_l = len(headers_ua)


def pause(t=0.5):
    time.sleep(np.random.rand()*t)


def url_to_id(url, cat="people"):
    '''
    cat can be: people, book, movie, music, game, play.
    '''
    if cat == "people":
        l = url.find("/people/")
        if url[-1:] == '/':
            return url[l+8:-1]
        else:
            return url[l+8:]

    if cat == "book" or cat == "movie" or cat == "music":
        l = url.find("/subject/")
        if url[-1:] == '/':
            return url[l+9:-1]
        else:
            return url[l+9:]


def get_rating(span):
    if not span.has_attr("class"):
        return 0
    st = span["class"][0]
    # print(st)
    if len(st) < 6:
        return 0
    return int(st[6])*2


if __name__ == "__main__":
    # print(url_to_id("https://www.douban.com/people/ikgendou/"))
    # print(url_to_id("https://www.douban.com/people/2783455"))
    soup = BeautifulSoup('<span class="rating5-t"></span>', "lxml")
    print(get_rating(soup.span))
