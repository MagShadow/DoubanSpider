import urllib
import requests
import time
import sys
import json
import numpy as np
from bs4 import BeautifulSoup
from bs_filters import *

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}]
headers_l = len(headers)


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
    s.post(login_url, headers=headers[0], data=data)
    # print(html)
    return s


def dig_user(user_id, s, recursive=False):
    homepage_url = f"https://www.douban.com/people/{user_id}/"
    # print(homepage_url)

    time.sleep(np.random.rand())
    r = s.get(homepage_url, headers=headers[0])
    soup = BeautifulSoup(r.text, "lxml")
    # with open("./test/user_login.html", "w") as f:
    #     f.write(soup.prettify())

    # 抓取个人基本信息
    user_info = dict()
    user_info["id"] = user_id
    user_info["name"] = soup.title.string.strip()
    sig = soup.find(is_signature)
    if 'a_edit_signature' in sig["class"]:
        user_info["sig"] = sig.span.string.strip()
    else:
        user_info["sig"] = sig.string.strip()
    intro = soup.find('textarea', {'name': 'intro'})
    user_info["intro"] = intro.string
    loc = soup.find('div', {'class': 'user-info'}).a
    user_info["loc"] = loc.string.strip()
    print(user_info)

    

if __name__ == "__main__":
    with open("./src/yang.json", "r") as f:
        user_json = json.load(f)

    dig_user(user_id=user_json["user"], s=login(
        "./src/yang.json"), recursive=True)
