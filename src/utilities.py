import re

headers_ua = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}]
headers_l = len(headers_ua)

def link_to_id(link, cat="people"):
    '''
    cat can be: people, book, movie, music, game, play.
    '''
    if cat == "people":
        l = link.find("/people/")
        if link[-1:] == '/':
            return link[l+8:-1]
        else:
            return link[l+8:]


if __name__ == "__main__":
    print(link_to_id("https://www.douban.com/people/ikgendou/"))
    print(link_to_id("https://www.douban.com/people/2783455"))
