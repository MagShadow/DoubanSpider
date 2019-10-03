from bs4 import BeautifulSoup
from utilities import *


def get_book_info(book_id, s):
    book_url = f"https://book.douban.com/subject/{book_id}/"
    pause()
    r = s.get(book_url, headers=headers_ua[0])
    soup_book = BeautifulSoup(r.text, "lxml")

    book_info = {"id": "", "name": "", "rating": 0}
    book_info["id"] = book_id
    try:
        w = soup_book.body.find("div", {"id": "wrapper"})
        book_info["name"] = w.h1.span.string.strip()
    except:
        book_info["name"] = soup_book.head.title.string.strip()[:-4]

    try:
        # print("looking for rating")
        target = soup_book.find("div", {"class": "rating_self clearfix"})
        # print(target.strong.string.strip())
        book_info["rating"] = float(target.strong.string.strip())
    except:
        pass

    return book_info


def get_book_list(url, s):
    temp_url = url
    index = 0
    full_list = []
    while True:
        pause()
        r = s.get(temp_url, headers=headers_ua[0])
        soup_book = BeautifulSoup(r.text, "lxml")

        book_list = soup_book.find_all("li", {"class": "subject-item"})
        for b in book_list:
            link = b.find("div", {"class": "info"}).h2.a
            print("Book:", link["title"])
            book_url = link["href"]
            # print(book_url)
            tar_book_id = url_to_id(book_url, cat="book")
            print(get_book_info(tar_book_id, s))

        full_list += book_list

        if len(book_list) < 15:
            break
        else:
            index += 15
            temp_url = url + \
                f"?start={str(index)}&sort=time&rating=all&filter=all&mode=grid"


def dig_user_book(user_id, s, is_self=False):
    do_url = f"https://book.douban.com/people/{user_id}/do"
    wish_url = f"https://book.douban.com/people/{user_id}/wish"
    collect_url = f"https://book.douban.com/people/{user_id}/collect"

    # get_book_list(do_url, s)
    get_book_list(wish_url, s)
    # get_book_list(collect_url, s)
