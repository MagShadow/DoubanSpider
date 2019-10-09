import re
import csv
import os
import time
import json
import requests

from datetime import datetime
import numpy as np

from bs4 import BeautifulSoup

headers_ua = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}]
headers_l = len(headers_ua)

with open(os.path.join("src", "config.json"), "r") as f:
    user_json = json.load(f)


def login(filename):
    login_url = "https://accounts.douban.com/j/mobile/login/basic"
    with open(filename, "r") as f:
        user_json = json.load(f)
    name, pswd = user_json["email"], user_json["pswd"]
    data = {
        'ck': '',
        "name": name,
        "password": pswd,
        'remember': 'true',
        'ticket': '',
    }
    s = requests.Session()
    s.post(login_url, headers=headers_ua[0], data=data)
    # print(html)
    return s


def get_response(s, url):
    pause()
    r = s.get(url, headers=headers_ua[0])
    soup = BeautifulSoup(r.text, "lxml")

    while soup.head.title.string.strip() == "禁止访问":
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!         Captcha          !")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print()
        print("Please use Browser to visit douban.com")
        x = input("Press any key after finished:")
        r = s.get(url, headers=headers_ua[0])
        soup = BeautifulSoup(r.text, "lxml")

    return soup


def pause(t=1):
    if user_json["waiting"] != 0:
        t = user_json["waiting"]
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


cat_set = set(["contact", "rcontact", "book",
               "movie", "music", "game", "drama", "friend"])


def data_exist(user_id, cat="contact", renew=1):
    '''
    Check filename: "./data/{user_id}/{user_id}_{cat}.csv";

    If the latest modify time is {renew} days advance of now, also need to update.
    '''
    assert cat in cat_set
    try:
        data_path = os.path.join("data", user_id)
        filename = os.path.join(data_path, f"{user_id}_{cat}.csv")
        if not os.path.isfile(filename):
            return False

        mtime = os.path.getmtime(filename)
        ntime = time.time()
        return (ntime-mtime) < renew*86400
    except:
        return False


def save(user_id, item_list, cat="contact"):
    '''
    Filename will be "./data/{user_id}/{user_id}_{cat}.csv";
    '''

    assert cat in cat_set
    if item_list == []:
        return
    data_path = os.path.join("data", user_id)
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    filename = os.path.join(data_path, f"{user_id}_{cat}.csv")
    if cat == "friend":
        with open(filename, "w") as f:
            for x in item_list:
                f.write(x + "\n")
        return

    if cat == "contact" or cat == "rcontact":
        header = ["id", "name"]
    else:
        header = ["id", "rating", "status"]

    with open(filename, "w") as f:
        f_csv = csv.DictWriter(f, header)
        f_csv.writeheader()
        f_csv.writerows(item_list)


def read(user_id, cat="contact"):
    assert cat in cat_set

    data_path = os.path.join("data", user_id)
    filename = os.path.join(data_path, f"{user_id}_{cat}.csv")
    full_list = []
    if cat != "friend":
        with open(filename, "r") as f:
            f_csv = csv.DictReader(f)
            for row in f_csv:
                full_list.append(dict(row))
    else:
        with open(filename, "r") as f:
            full_list = f.readlines()

    return full_list


with open("./src/template.html", "r") as f:
    template_html = f.read()


def generate_html(filename="test.html", title="Douban", content=[]):
    soup = BeautifulSoup(template_html, "lxml")
    article = soup.find("div", {"class": "article"})
    for c in content:
        article.append(c)

    data_path = os.path.join("data", filename)
    with open(data_path, "w") as f:
        f.write(soup.prettify())


if __name__ == "__main__":
    # print(url_to_id("https://www.douban.com/people/ikgendou/"))
    # print(url_to_id("https://www.douban.com/people/2783455"))
    # soup = BeautifulSoup('<span class="rating-star allstar40"></span>', "lxml")
    # print(get_rating(soup.span))
    print()
