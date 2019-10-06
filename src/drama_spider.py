from bs4 import BeautifulSoup
from utilities import *


def get_drama_info(drama_id, s):
    drama_url = f"https://www.douban.com/location/drama/{drama_id}/"
    soup_drama = get_response(s, drama_url)

    drama_info = {"id": "", "name": "", "rating": 0}
    drama_info["id"] = drama_id
    try:
        m = soup_drama.body.find("div", {"class": "meta"})
        drama_info["name"] = m.h1.span.string.strip()
    except:
        drama_info["name"] = soup_drama.head.title.string.strip()[:-10]

    try:
        # print("looking for rating")

        target = soup_drama.body.find("div", {"class": "meta"})

        # print(target)
        # print(target.div.strong.string.strip())
        drama_info["rating"] = float(target.div.strong.string.strip())
    except:
        pass

    return drama_info


def get_drama_list(url, s, get_detail=False):
    temp_url = url
    index = 0
    full_list = []
    while True:
        soup_drama = get_response(s, temp_url)

        drama_list = soup_drama.find_all("div", {"class": "item"})
        for b in drama_list:
            link = b.find("div", {"class": "info"}).ul.li.a
            print("drama:", link.em.string.strip())
            drama_url = link["href"]
            # print(drama_url)
            tar_drama_id = url_to_id(drama_url, cat="drama")
            try:
                sp = b.find("li", {"class": "intro"}
                            ).next_sibling.next_sibling.span
                rating = get_rating(sp)
            except:
                rating = 0
            full_list.append((tar_drama_id, rating))

            if get_detail:
                get_drama_info(tar_drama_id, s)

        if len(drama_list) < 15:
            break
        else:
            index += 15
            temp_url = url + \
                f"?start={str(index)}&sort=time&mode=grid&rating=all"
            # print(temp_url)

    return full_list


def dig_user_drama(user_id, s, is_self=False):
    if data_exist(user_id, cat="drama"):
        return
    wish_url = f"https://www.douban.com/location/people/{user_id}/drama/wish"
    collect_url = f"https://www.douban.com/location/people/{user_id}/drama/collect"

    wish_list = get_drama_list(wish_url, s)
    collect_list = get_drama_list(collect_url, s)
    drama_list = []

    for item in wish_list:
        drama_list.append({"id": item[0], "rating": item[1], "status": "wish"})
    for item in collect_list:
        drama_list.append(
            {"id": item[0], "rating": item[1], "status": "collect"})

    save(user_id, drama_list, "drama")
