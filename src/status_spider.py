from utilities import *
from bs4 import BeautifulSoup
from user_spider import dig_user


def get_user_status(tar_user_id, s, time_window=86400):
    assert time_window > 0

    now = time.time()

    tar_url = f"https://www.douban.com/people/{tar_user_id}/statuses"
    page = 1
    temp_url = tar_url
    full_list = []

    is_near = True
    while is_near:
        soup = get_response(s, temp_url)
        status_list = soup.find_all(
            "div", {"class": "status-wrapper"})
        if status_list == []:
            break
        for status in status_list:
            try:
                span = status.find("span", {"class": "created_at"})
                # print(span["title"])
                create_time = datetime.strptime(
                    span["title"], r"%Y-%m-%d %H:%M:%S")
                # print(create_time)
                if (now-create_time.timestamp()) > time_window:
                    is_near = False
                    break
                full_list.append({"content": status, "time": create_time})
                # print(status)
            except:
                is_near = False

        page += 1
        temp_url = tar_url+"?p="+str(page)

    return full_list


def collect_status(user_id, s, time_window, filename="status.html"):
    dig_user(user_id, s, recursive=False)
    contact_list = read(user_id, "contact")
    status_list = []
    for c in contact_list:
        print("Collect Status of User:", c["name"])
        status = get_user_status(c["id"], s, time_window)
        status_list += status
        print("Number of New Status:", len(status))

    status_list.sort(key=lambda s: s["time"], reverse=True)
    generate_html(filename=filename, title="Douban",
                  content=[x["content"] for x in status_list])
