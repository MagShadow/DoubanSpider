from bs4 import BeautifulSoup
from utilities import *


def get_movie_info(movie_id, s):
    movie_url = f"https://movie.douban.com/subject/{movie_id}/"
    pause()
    r = s.get(movie_url, headers=headers_ua[0])
    soup_movie = BeautifulSoup(r.text, "lxml")

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


def get_movie_list(url, s):
    temp_url = url
    index = 0
    full_list = []
    while True:
        pause()
        r = s.get(temp_url, headers=headers_ua[0])
        soup_movie = BeautifulSoup(r.text, "lxml")

        movie_list = soup_movie.find_all("div", {"class": "item"})
        for b in movie_list:
            link = b.find("div", {"class": "info"}).ul.li.a
            print("movie:", link.em.string.strip())
            movie_url = link["href"]
            # print(movie_url)
            tar_movie_id = url_to_id(movie_url, cat="movie")
            # print(get_movie_info(tar_movie_id, s))

            try:
                ul = b.find("ul")
                sp = ul.li.next_sibling.next_sibling.next_sibling.next_sibling.span
                # 同级列表中的<li></li>，连接时第一个next_sibling会指向中间的分隔符
                # 见https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/next-sibling-previous-sibling
                rating = get_rating(sp)
            except:
                rating = 0
            full_list.append((tar_movie_id, rating))

        # full_list += movie_list

        if len(movie_list) < 15:
            break
        else:
            index += 15
            temp_url = url + \
                f"?start={str(index)}&sort=time&rating=all&filter=all&mode=grid"
    return full_list


def dig_user_movie(user_id, s, is_self=False):
    do_url = f"https://movie.douban.com/people/{user_id}/do"
    wish_url = f"https://movie.douban.com/people/{user_id}/wish"
    collect_url = f"https://movie.douban.com/people/{user_id}/collect"

    # do_list = get_movie_list(do_url, s)
    # get_movie_list(wish_url, s)
    collect_list = get_movie_list(collect_url, s)

    print(len(collect_list))
    for item in collect_list:
        print(item[0], "Rating:", item[1])
