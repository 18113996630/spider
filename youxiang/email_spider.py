# -*- coding: UTF-8 -*-
from urllib.parse import urlencode

import requests
from pyquery import PyQuery as pq


def get_index(url):
    response = requests.get(url)
    if response.status_code == 200:
        text = response.text
        return text
    return None


def parse_index_html(html):
    if html is None:
        return


if __name__ == '__main__':
    print(get_index("http://www.hao123.com/mail"))
