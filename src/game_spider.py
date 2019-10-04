from bs4 import BeautifulSoup
from utilities import *


def get_game_info(game_id, s):
    game_url = f"https://www.douban.com/game/{game_id}/"
    pause()
    r = s.get(game_url, headers=headers_ua[0])
    soup_game = BeautifulSoup(r.text, "lxml")

    game_info = {"id": "", "name": "", "rating": 0}
    game_info["id"] = game_id
    try:
        w = soup_game.body.find("div", {"id": "wrapper"})
        game_info["name"] = w.div.h1.span.string.strip()
    except:
        game_info["name"] = soup_game.head.title.string.strip()[:-4]

    try:
        # print("looking for rating")
        target = soup_game.find("div", {"class": "rating_self clearfix"})
        # print(target.strong.string.strip())
        game_info["rating"] = float(target.strong.string.strip())
    except:
        pass

    return game_info


def get_game_list(url, s):
    temp_url = url
    index = 0
    full_list = []
    while True:
        pause()
        r = s.get(temp_url, headers=headers_ua[0])
        soup_game = BeautifulSoup(r.text, "lxml")

        game_list = soup_game.find_all("div", {"class": "common-item"})

        for b in game_list:
            link = b.find("div", {"class": "content"}).div.a
            print("game:", link.string.strip())
            game_url = link["href"]
            # print(game_url)
            tar_game_id = url_to_id(game_url, cat="game")
            print(get_game_info(tar_game_id, s))

            try:
                d = b.find("div", {"class": "rating-info"})
                rating = get_rating(d.span)
            except:
                rating = 0
            full_list.append((tar_game_id, rating))

        if len(game_list) < 15:
            break
        else:
            index += 15
            temp_url = url + "?action=collect&start=" + str(index)
            # print(temp_url)

    return full_list


def dig_user_game(user_id, s, is_self=False):
    do_url = f"https://www.douban.com/people/{user_id}/games?action=do"
    wish_url = f"https://www.douban.com/people/{user_id}/games?action=wish"
    collect_url = f"https://www.douban.com/people/{user_id}/games?action=collect"

    # do_list = get_game_list(do_url, s)
    # wish_list = get_game_list(wish_url, s)
    collect_list = get_game_list(collect_url, s)
    print(len(collect_list))
    for item in collect_list:
        print(item[0], "Rating:", item[1])