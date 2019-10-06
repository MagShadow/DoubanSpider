from bs4 import BeautifulSoup
from utilities import *


def get_movie_info(movie_id, s):
    movie_url = f"https://movie.douban.com/subject/{movie_id}/"
    soup_movie = get_response(s, movie_url)

    movie_info = {"id": "", "name": "", "rating": 0}
    movie_info["id"] = movie_id
    try:
        w = soup_movie.body.find("div", {"id": "wrapper"})
        movie_info["name"] = w.h1.span.string.strip()
    except:
        movie_info["name"] = soup_movie.head.title.string.strip()[:-4]

    try:
        # print("looking for rating")
        target = soup_movie.find("div", {"class": "rating_self clearfix"})
        # print(target.strong.string.strip())
        movie_info["rating"] = float(target.strong.string.strip())
    except:
        pass

    return movie_info


def get_movie_list(url, s, get_detail=False):
    temp_url = url
    index = 0
    full_list = []
    while True:
        soup_movie = get_response(s, temp_url)

        movie_list = soup_movie.find_all("div", {"class": "item"})
        for b in movie_list:
            link = b.find("div", {"class": "info"}).ul.li.a
            print("movie:", link.em.string.strip())
            movie_url = link["href"]
            # print(movie_url)
            tar_movie_id = url_to_id(movie_url, cat="movie")

            try:
                ul = b.find("ul")
                sp = ul.li.next_sibling.next_sibling.next_sibling.next_sibling.span
                # 同级列表中的<li></li>，连接时第一个next_sibling会指向中间的分隔符
                # 见https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/next-sibling-previous-sibling
                rating = get_rating(sp)
            except:
                rating = 0
            full_list.append((tar_movie_id, rating))

            if get_detail:
                get_movie_info(tar_movie_id, s)

        # full_list += movie_list

        if len(movie_list) < 15:
            break
        else:
            index += 15
            temp_url = url + \
                f"?start={str(index)}&sort=time&rating=all&filter=all&mode=grid"
    return full_list


def dig_user_movie(user_id, s, is_self=False):
    if data_exist(user_id, cat="movie"):
        return
    do_url = f"https://movie.douban.com/people/{user_id}/do"
    wish_url = f"https://movie.douban.com/people/{user_id}/wish"
    collect_url = f"https://movie.douban.com/people/{user_id}/collect"

    do_list = get_movie_list(do_url, s)
    wish_list = get_movie_list(wish_url, s)
    collect_list = get_movie_list(collect_url, s)

    movie_list = []
    for item in do_list:
        movie_list.append({"id": item[0], "rating": item[1], "status": "do"})
    for item in wish_list:
        movie_list.append({"id": item[0], "rating": item[1], "status": "wish"})
    for item in collect_list:
        movie_list.append(
            {"id": item[0], "rating": item[1], "status": "collect"})

    save(user_id, movie_list, "movie")
