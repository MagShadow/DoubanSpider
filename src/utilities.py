import re
import csv
import os
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

    if cat == "game":
        l = url.find("/game/")
        if url[-1:] == '/':
            return url[l+6:-1]
        else:
            return url[l+6:]

    if cat == "drama":
        l = url.find("/drama/")
        if url[-1:] == '/':
            return url[l+7:-1]
        else:
            return url[l+7:]


def get_rating(span):
    if not span.has_attr("class"):
        return 0
    st = span["class"][0]
    # print(st)
    if len(st) < 6 or not "rating" in st:
        return 0
    # print(st)
    if "star" in st:
        return int(span["class"][1][7])*2
    else:
        return int(st[6])*2


def save(user_id, item_list, cat="contact"):
    '''
    Filename will be "./data/{user_id}/{user_id}_{cat}.csv";
    '''
    cat_set = set("contact", "rcontact", "book",
                  "movie", "music", "game", "drama")
    assert cat in cat_set

    data_path = os.path.join("data", user_id)
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    filename = os.path.join(data_path, f"{user_id}_{cat}.csv")

    if cat == "contact" or cat == "rcontact":
        header = ["id", "name", "loc", "sig", "intro"]
    else:
        header = ["id", "rating", "status"]

    with open(filename, "w") as f:
        f_csv = csv.DictWriter(f, header)
        f_csv.writeheader()
        f_csv.writerows(item_list)


if __name__ == "__main__":
    # print(url_to_id("https://www.douban.com/people/ikgendou/"))
    # print(url_to_id("https://www.douban.com/people/2783455"))
    # soup = BeautifulSoup('<span class="rating-star allstar40"></span>', "lxml")
    # print(get_rating(soup.span))
    save("ikgendou", [], "contact")
