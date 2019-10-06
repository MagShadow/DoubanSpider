from bs4 import BeautifulSoup
from utilities import *


def get_game_info(game_id, s):
    game_url = f"https://www.douban.com/game/{game_id}/"
    soup_game = get_response(s, game_url)

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


def get_game_list(url, s, get_detail=False):
    temp_url = url
    index = 0
    full_list = []
    while True:
        soup_game = get_response(s, temp_url)

        game_list = soup_game.find_all("div", {"class": "common-item"})

        for b in game_list:
            link = b.find("div", {"class": "content"}).div.a
            print("game:", link.string.strip())
            game_url = link["href"]
            # print(game_url)
            tar_game_id = url_to_id(game_url, cat="game")

            try:
                d = b.find("div", {"class": "rating-info"})
                rating = get_rating(d.span)
            except:
                rating = 0
            full_list.append((tar_game_id, rating))

            if get_detail:
                get_game_info(tar_game_id, s)

        if len(game_list) < 15:
            break
        else:
            index += 15
            temp_url = url + "?action=collect&start=" + str(index)
            # print(temp_url)

    return full_list


def dig_user_game(user_id, s, is_self=False):
    if data_exist(user_id, cat="game"):
        return
    do_url = f"https://www.douban.com/people/{user_id}/games?action=do"
    wish_url = f"https://www.douban.com/people/{user_id}/games?action=wish"
    collect_url = f"https://www.douban.com/people/{user_id}/games?action=collect"

    do_list = get_game_list(do_url, s)
    wish_list = get_game_list(wish_url, s)
    collect_list = get_game_list(collect_url, s)

    game_list = []
    for item in do_list:
        game_list.append({"id": item[0], "rating": item[1], "status": "do"})
    for item in wish_list:
        game_list.append({"id": item[0], "rating": item[1], "status": "wish"})
    for item in collect_list:
        game_list.append(
            {"id": item[0], "rating": item[1], "status": "collect"})

    save(user_id, game_list, "game")
