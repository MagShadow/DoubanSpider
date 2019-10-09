import urllib
import time
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





def login_2(filename):
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

    soup = get_response(s, url)
    user_info = {"id": "", "name": "", "loc": "", "sig": "", "intro": ""}
    try:
        user_info["id"] = user_id
        user_info["name"] = soup.title.string.strip()
        intro = soup.find('textarea', {'name': 'intro'})
        user_info["intro"] = intro.string
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
    # if data_exist(user_id, cat="contact"):
    #     return
    temp_url = url

    index = 0
    # with open("./test/self_contact.html", "w") as f:
    #     f.write(soup_contact.prettify())
    full_list = []
    while True:
        soup_contact = get_response(s, temp_url)

        user_list = soup_contact.find(
            "ul", {"class": "user-list"}).find_all("li", {"class": "clearfix"})
        for u in user_list:
            name = u.div.h3.a.string
            print("User:", name)
            user_url = u.a["href"]
            tar_user_id = url_to_id(user_url)
            tar_user_info = {"id": tar_user_id,
                             "name": name}
            # print(tar_user_info)
            full_list.append(tar_user_info)

        if len(user_list) < 20:
            break
        else:
            index += 20
            temp_url = url+"?tag=0&start=" + str(index)

    return full_list


def get_other_contact_list(url, s):
    # if data_exist(user_id, cat="rcontact"):
    #     return
    temp_url = url

    index = 0
    full_list = []

    soup_contact = get_response(s, temp_url)
    if (soup_contact.find("div", {"id": "db-timeline-hd"})) != None or (soup_contact.find("ul", {"class": "user-list"}) != None):
        if url[-12:] == "rev_contacts":
            return get_self_contact_list("https://www.douban.com/contacts/rlist", s)
        else:
            return get_self_contact_list("https://www.douban.com/contacts/list", s)

    more_than_1page = False
    try:
        navi = soup_contact.find("div", {"class": "paginator"})
        if navi != None:
            more_than_1page = True
    except:
        pass

    if not more_than_1page:
        user_list = soup_contact.find_all("dl", {"class": "obu"})
        for u in user_list:
            name = u.dd.a.string
            print("User:", name)
            user_url = u.dd.a["href"]
            tar_user_id = url_to_id(user_url)
            # tar_user_info = get_user_info(tar_user_id, s)
            # print(tar_user_info)
            tar_user_info = {"id": tar_user_id, "name": name}
            full_list.append(tar_user_info)
    else:
        while True:
            user_list = soup_contact.find_all("dl", {"class": "obu"})
            for u in user_list:
                name = u.dd.a.string
                print("User:", name)
                user_url = u.dd.a["href"]
                tar_user_id = url_to_id(user_url)
                # tar_user_info = get_user_info(tar_user_id, s)
                # print(tar_user_info)
                tar_user_info = {"id": tar_user_id, "name": name}
                full_list.append(tar_user_info)

            if len(user_list) < 70:
                break
            else:
                index += 70
                temp_url = url+"?start=" + str(index)

            soup_contact = get_response(s, temp_url)

    return full_list


def dig_user_contact(user_id, s, cat="contact"):
    assert cat in ["contact", "rcontact"]

    if data_exist(user_id, cat=cat):
        print(f"Use existed {cat} data!")
        return read(user_id, cat=cat)

    homepage_url = f"https://www.douban.com/people/{user_id}/"
    if cat == "contact":
        url = homepage_url+"contacts"
    else:
        url = homepage_url+"rev_contacts"
    full_list = get_other_contact_list(url, s)
    save(user_id, full_list, cat)

    return full_list

    # if is_self:
    #     contact_url = "https://www.douban.com/contacts/list"
    #     rcontact_url = "https://www.douban.com/contacts/rlist"
    #     contact_list = get_self_contact_list(contact_url, s)
    #     rcontact_list = get_self_contact_list(rcontact_url, s)

    #     save(user_id, contact_list, "contact")
    #     save(user_id, rcontact_list, "rcontact")

    # else:


def dig_user(user_id, s, recursive=False):
    try:
        # 抓取个人基本信息
        user_info = get_user_info(user_id, s)
        print(user_info)
        # 如果title抓出来是豆瓣，说明该用户已经注销
        if user_info["name"] == "豆瓣":
            return False

        # 抓取图书列表
        dig_user_book(user_id, s)

        # 抓取影视列表
        dig_user_movie(user_id, s)

        # 抓取音乐列表
        dig_user_music(user_id, s)

        # 抓取游戏列表
        dig_user_game(user_id, s)

        # 抓取舞台剧列表
        dig_user_drama(user_id, s)

        # Collect Contact/Rev_Contact Info
        # 自己看自己的关注/被关注列表和自己看别人的关注/被关注列表是不一样的

        contact_list = dig_user_contact(user_id, s, cat="contact")
        rcontact_list = dig_user_contact(user_id, s, cat="rcontact")
        # print(contact_list)
        contact_id_set = set([x["id"] for x in contact_list])
        rcontact_id_set = set([x["id"] for x in rcontact_list])

        friend_id_list = list(contact_id_set & rcontact_id_set)
        friend_id_list.sort()

        save(user_id, friend_id_list, "friend")

        if recursive:
            for friend_id in friend_id_list:
                dig_user(friend_id, s)
    except Exception as e:
        print(f"Error when collect {user_id}!")
        print(str(e))


if __name__ == "__main__":
    with open("./src/config.json", "r") as f:
        user_json = json.load(f)
    se = login("./src/config.json")

    # dig_user(user_id=user_json["user"], s=login(
    # "./src/config.json"), recursive=True)
    # print(get_book_info(book_id="10771256", s=login("./src/yang.json")))
    # dig_user(user_id="175563657", s=login(
    #     "./src/yang.json"), is_self=False, recursive=False)
    # from status_spider import *
    # # status_list = get_user_status("Ice.Nefar", s=se, time_window=86400*5)
    # # print(status_list)
    # collect_status(user_id=user_json["user"], s=se, time_window=86400 *
    #                5, filename="status.html")
    # r = se.get("https://www.douban.com")
    # with open("./test/homepage.html", "w") as f:
    #     f.write(r.text)
