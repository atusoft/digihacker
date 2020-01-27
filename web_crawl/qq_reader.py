import requests
import os
import sqlite3
import requests
from win32.win32crypt import CryptUnprotectData
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup as bs
import redis
import time
import random
import sys

cookie = ''
r = redis.Redis(host='192.168.1.250', port=6379, decode_responses=True)


class UserEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Book):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def object_decoder(obj):
    print(f"decoder:{obj}")
    # if '__type__' in obj and obj['__type__'] == 'User':
    return Book(obj['title'], obj['link'], obj['rate'], obj['review'])


# return obj


def get_cookie_from_chrome(host):
    cookie_path = os.environ['LOCALAPPDATA'] + r"\Google\Chrome\User Data\Default\Cookies"
    sql = "select host_key,name,encrypted_value from cookies where host_key='%s'" % host
    with sqlite3.connect(cookie_path) as conn:
        cu = conn.cursor()
        cookies = {name: CryptUnprotectData(encrypted_value)[1].decode() for host_key, name, encrypted_value in
                   cu.execute(sql).fetchall()}
        # for host_key, name, encrypted_value in cu.execute(sql).fetchall():
        #     print(f"{host_key}:{name}")
        return cookies


def get_page(url):
    global cookie
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
    result = requests.get(url, cookies=cookie, headers=headers)
    result.encoding = 'utf-8'
    return result.text


def download_shelf():
    html = get_page("https://weread.qq.com/web/shelf")
    with open("shelf.html", "w", encoding='utf-8') as f:
        f.write(html)


def get_detail(book, refresh=False):
    saved_book = r.get(book.title)
    # if refresh or not saved_book:
    #     load_detail(book)
    # else:
    if (saved_book):
        newbook = json.loads(saved_book, object_hook=object_decoder)
        return newbook
    return book


def load_detail(book):
    try:
        time.sleep(random.randint(1, 60))
        html = get_page(book.link)
        # save_html(book)

        html = bs(html, features="lxml")
        book.rate = html.select("span.bookInfo_more_line1_number")[0].text
        book.reviewer = html.select(".bookInfo_more_line2")[0].text
        r.set(book.title, json.dumps(book, cls=UserEncoder))
    except Exception as e:
        print(e)


def save_html(book):
    cache_file = book.title + ".html"
    if Path(cache_file).is_file():
        with open(cache_file) as f:
            html = f.read()
    else:
        with open(book.title + ".html", "w") as f:
            html = get_page(book.link)
            if len(html) > 0:
                f.write(html)
    return html


class Book:
    title = ""
    link = ""
    rate = ""
    reviewer = ""

    def __init__(self, link, title, rate="", reviewer=""):
        self.title = title
        self.link = link
        self.rate = rate
        self.reviewer = reviewer

    def __str__(self):
        return f"{self.title}:{self.rate}:{self.reviewer}"


if __name__ == '__main__':

    root = "https://weread.qq.com"
    cookie = get_cookie_from_chrome('.weread.qq.com')
    download_shelf()
    with open('shelf.html', encoding='utf-8') as f:
        html_string = f.read()
        html = bs(html_string, features="lxml")
        shelf = html.select(".shelf_list")[0]
        shelfBooks = shelf.find_all(attrs={'class': 'shelfBook'})
        books = []
        for b in shelfBooks:
            try:
                books.append(Book(root + b.get('href'), b.select('div.title')[0].text))
            except Exception as e:
                print(f"{b} got {e}")
    for b in books:
        bs = get_detail(b, refresh=False)
        if type(bs) is not Book:
            if '8.' in bs.split(':')[1]:
                print(bs)
            if '万' in bs.split(':')[1]:
                print(bs)
