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
time.sleep(np.random.rand()*5)


def dig_user(user_id, recursive=False):
    homepage_url = f"https://www.douban.com/people/{user_id}/"
    # print(homepage_url)

    time.sleep(np.random.rand()*5)
    r = requests.get(
        homepage_url, headers=headers[int(np.random.rand()*headers_l)])  # 随机选择一个user-agent
    soup = BeautifulSoup(r.text, "lxml")

    user_info = dict()
    user_info["id"] = user_id
    user_info["name"] = soup.title.string.strip()
    sig = soup.find('div', {'class': 'signature_display pl'})
    user_info["sig"] = sig.string.strip()
    intro = soup.find('textarea', {'name': 'intro'})
    user_info["intro"] = intro.string
    loc = soup.find('div', {'class': 'user-info'}).a
    user_info["loc"] = loc.string.strip()
    print(user_info)


if __name__ == "__main__":
    with open("./src/yang.json", "r") as f:
        user_json = json.load(f)

    dig_user(user_id=user_json["user"], recursive=True)
