# -*- coding: UTF-8 -*-
import json
import logging
import re
from multiprocessing import Pool

import requests


def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.RequestException as e:
        logging.error(e.strerror)
        return None


def parse_content(html):
    regex = '<dd>.*?board-index.*?">(\d+)</i>.*?title="(.*?)".*?data-src="(.*?)".*?class="star">(' \
            '.*?)</p>.*?class="releasetime">(.*?)</p>' \
            '.*?class="integer">(.*?)</i>.*?class="fraction">(.*?)</i>.*?</dd>'
    # regex = '<dd>.*?board-index'
    patten = re.compile(regex, re.S)
    # [('1', '霸王别姬', 'https://p1.meituan.net/movie/20803f59291c47e1e116c11963ce019e68711.jpg@160w_220h_1e_1c',
    #   '\n                主演：张国荣,张丰毅,巩俐\n        ', '上映时间：1993-01-01', '9.', '5')]
    items = re.findall(patten, html)
    for item in items:
        yield {
            'index': item[0],
            'title': item[1],
            'img': item[2],
            'star': str(item[3]).strip()[3:],
            'time': item[4][5:],
            'score': item[5] + item[6]
        }


def write_to_file(data):
    with open('top100.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')


def main(i):
    base_url = "https://maoyan.com/board/4?offset="
    for offset in range(0, 100, 10):
        url = base_url + str(offset)
        html = get_one_page(url)
        for data in parse_content(html):
            write_to_file(data)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, ([i for i in range(1)]))
