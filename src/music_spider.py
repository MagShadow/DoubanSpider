from bs4 import BeautifulSoup
from utilities import *


def get_music_info(music_id, s):
    music_url = f"https://music.douban.com/subject/{music_id}/"
    soup_music = get_response(s, music_url)

    music_info = {"id": "", "name": "", "rating": 0}
    music_info["id"] = music_id
    try:
        w = soup_music.body.find("div", {"id": "wrapper"})
        music_info["name"] = w.h1.span.string.strip()
    except:
        music_info["name"] = soup_music.head.title.string.strip()[:-4]

    try:
        # print("looking for rating")
        target = soup_music.find("div", {"class": "rating_self clearfix"})
        # print(target.strong.string.strip())
        music_info["rating"] = float(target.strong.string.strip())
    except:
        pass

    return music_info


def get_music_list(url, s, get_detail=False):
    temp_url = url
    index = 0
    full_list = []
    while True:
        soup_music = get_response(s, temp_url)

        music_list = soup_music.find_all("div", {"class": "item"})

        for b in music_list:
            link = b.find("div", {"class": "info"}).ul.li.a
            print("music:", link.em.string.strip())
            music_url = link["href"]
            # print(music_url)
            tar_music_id = url_to_id(music_url, cat="music")
            # print(get_music_info(tar_music_id, s))

            try:
                ul = b.find("ul")
                sp = ul.li.next_sibling.next_sibling.next_sibling.next_sibling.span
                # 同级列表中的<li></li>，连接时第一个next_sibling会指向中间的分隔符
                # 见https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/next-sibling-previous-sibling
                rating = get_rating(sp)
            except:
                rating = 0
            full_list.append((tar_music_id, rating))

            if get_detail:
                get_music_info(tar_music_id, s)

        if len(music_list) < 15:
            break
        else:
            index += 15
            temp_url = url + \
                f"?start={str(index)}&sort=time&rating=all&filter=all&mode=grid"
            # print(temp_url)

    return full_list


def dig_user_music(user_id, s, is_self=False):
    if data_exist(user_id, cat="music"):
        return
    do_url = f"https://music.douban.com/people/{user_id}/do"
    wish_url = f"https://music.douban.com/people/{user_id}/wish"
    collect_url = f"https://music.douban.com/people/{user_id}/collect"

    do_list = get_music_list(do_url, s)
    wish_list = get_music_list(wish_url, s)
    collect_list = get_music_list(collect_url, s)

    music_list = []
    for item in do_list:
        music_list.append({"id": item[0], "rating": item[1], "status": "do"})
    for item in wish_list:
        music_list.append({"id": item[0], "rating": item[1], "status": "wish"})
    for item in collect_list:
        music_list.append(
            {"id": item[0], "rating": item[1], "status": "collect"})

    save(user_id, music_list, "music")
