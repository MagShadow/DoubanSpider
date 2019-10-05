import urllib
import requests
import time
import sys
import json

import numpy as np
from bs4 import BeautifulSoup
from bs_filters import *
from utilities import *
from book_spider import dig_user_book
from movie_spider import dig_user_movie
from music_spider import dig_user_music
from game_spider import dig_user_game
from drama_spider import dig_user_drama


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


def get_user_info(user_id, s):
    url = f"https://www.douban.com/people/{user_id}/"
    r = s.get(url, headers=headers_ua[0])
    soup = BeautifulSoup(r.text, "lxml")
    user_info = {"id": "", "name": "",  "loc": "", "sig": ""}
    try:
        user_info["id"] = user_id
        user_info["name"] = soup.title.string.strip()
        # intro = soup.find('textarea', {'name': 'intro'})
        # user_info["intro"] = intro.string
    except Exception as e:
        pass

    try:
        loc = soup.find('div', {'class': 'user-info'}).a
        user_info["loc"] = loc.string.strip()
    except Exception as e:
        pass

    try:
        sig = soup.find(is_signature)
        if 'a_edit_signature' in sig["class"]:
            user_info["sig"] = sig.span.string.strip()
        else:
            user_info["sig"] = sig.string.strip()
    except Exception as e:
        pass

    return user_info


def get_self_contact_list(url, s):
    temp_url = url

    index = 0
    # with open("./test/self_contact.html", "w") as f:
    #     f.write(soup_contact.prettify())
    full_list = []
    while True:
        pause()
        r = s.get(temp_url, headers=headers_ua[0])
        soup_contact = BeautifulSoup(r.text, "lxml")

        user_list = soup_contact.find(
            "ul", {"class": "user-list"}).find_all("li", {"class": "clearfix"})
        for u in user_list:
            print("User:", u.div.h3.a.string)
            user_url = u.a["href"]
            tar_user_id = url_to_id(user_url)
            tar_user_info = get_user_info(tar_user_id, s)
            print(tar_user_info)
            full_list.append(tar_user_info)

        if len(user_list) < 20:
            break
        else:
            index += 20
            temp_url = url+"?tag=0&start=" + str(index)

    return full_list


def dig_user(user_id, s, is_self=False, recursive=False):
     # 抓取个人基本信息
    user_info = get_user_info(user_id, s)
    print(user_info)
    # 如果title抓出来是豆瓣，说明该用户已经注销
    if user_info["name"] == "豆瓣":
        return False

    # # 抓取图书列表
    # dig_user_book(user_id, s)

    # # 抓取影视列表
    # dig_user_movie(user_id, s)

    # # 抓取音乐列表
    # dig_user_music(user_id, s)

    # # 抓取游戏列表
    # dig_user_game(user_id, s)

    # # 抓取舞台剧列表
    # dig_user_drama(user_id, s)

    # print(homepage_url)

    # 自己看自己的关注/被关注列表和自己看别人的关注/被关注列表是不一样的

    if is_self:
        contact_url = "https://www.douban.com/contacts/list"
        rcontact_url = "https://www.douban.com/contacts/rlist"
        contact_list = get_self_contact_list(contact_url, s)
        rcontact_list = get_self_contact_list(rcontact_url, s)

        save(user_id, contact_list, "contact")
        save(user_id, rcontact_list, "rcontact")

    else:
        homepage_url = f"https://www.douban.com/people/{user_id}/"
        contact_url = homepage_url+"contacts"
        rev_contact_url = homepage_url+"rev_contacts"

    # with open("./test/user_login.html", "w") as f:
    #     f.write(soup.prettify())

    if recursive == False:
        return
    # Collect Contact/Rev_Contact Info


if __name__ == "__main__":
    with open("./src/yang.json", "r") as f:
        user_json = json.load(f)

    dig_user(user_id=user_json["user"], s=login(
        "./src/yang.json"), is_self=True, recursive=False)
    # print(get_book_info(book_id="10771256", s=login("./src/yang.json")))
    # dig_user(user_id="175563657", s=login(
    #     "./src/yang.json"), is_self=False, recursive=False)
