from utilities import *
from user_spider import dig_user


def cos_sim(clist):
    for x in clist:
        if x["rating1"]*x["rating2"] == 0:
            clist.remove(x)  # 移除全部的想看/在看等无评分项

    # 豆瓣的五档制评分2~10不是一个好的标度
    # 这里重新定标到-4~4
    vec1 = np.array([x["rating1"]-4 for x in clist])
    vec2 = np.array([x["rating2"]-4 for x in clist])
    # print(vec1)
    # print(vec2)
    cos = np.dot(vec1, vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec1))
    sim = 0.5+0.5*cos
    return sim


def find_overlap(user_id_1, user_id_2, cat="friend"):
    assert cat in cat_set

    if cat == "friend":
        list1 = read(user_id_1, cat="friend")
        list2 = read(user_id_2, cat="friend")

        cross_list = list(set(list1) & set(list2))
        return cross_list

    if cat in {"contact", "rcontact"}:
        list1 = [x["id"] for x in read(user_id_1, cat=cat)]
        list2 = [x["id"] for x in read(user_id_2, cat=cat)]
        cross_list = list(set(list1) & set(list2))
        return cross_list

    list1 = read(user_id_1, cat=cat)
    list2 = read(user_id_2, cat=cat)

    id_list1 = [x["id"] for x in list1]
    id_list2 = [x["id"] for x in list2]
    id_cross_set = set(id_list1) & set(id_list2)

    clear_list1 = []
    for x in list1:
        if x["id"] in id_cross_set:
            clear_list1.append(x)
    clear_list2 = []
    for x in list2:
        if x["id"] in id_cross_set:
            clear_list2.append(x)
    clear_list1.sort(key=lambda x: x["id"])
    clear_list2.sort(key=lambda x: x["id"])

    cross_list = []
    for i in range(len(id_cross_set)):
        assert clear_list1[i]["id"] == clear_list2[i]["id"]
        item = {"id": clear_list1[i]["id"], "rating1": int(
            clear_list1[i]["rating"]), "rating2": int(clear_list2[i]["rating"])}
        cross_list.append(item)
    return cross_list


def compare(s, user_id_1, user_id_2):
    dig_user(user_id_1, s)
    dig_user(user_id_2, s)

    clist_book = find_overlap(user_id_1, user_id_2, "book")
    clist_movie = find_overlap(user_id_1, user_id_2, "movie")
    clist_music = find_overlap(user_id_1, user_id_2, "music")
    clist_game = find_overlap(user_id_1, user_id_2, "game")
    clist_drama = find_overlap(user_id_1, user_id_2, "drama")
    clist_contact = find_overlap(user_id_1, user_id_2, "contact")
    clist_rcontact = find_overlap(user_id_1, user_id_2, "rcontact")
    clist_friend = find_overlap(user_id_1, user_id_2, "friend")

    sim = cos_sim(clist_book+clist_movie+clist_music+clist_game+clist_drama)

    return {"clist_book": clist_book, "clist_movie": clist_movie, "clist_music": clist_music, "clist_game": clist_game, "clist_drama": clist_drama, "clist_contact": clist_contact, "clist_rcontact": clist_rcontact, "clist_friend": clist_friend, "sim": sim}


if __name__ == "__main__":
    se = login("./src/config.json")
    print(compare(se, user_json["user"], "neptunedawn"))
