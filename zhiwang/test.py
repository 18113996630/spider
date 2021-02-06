# -*- coding: UTF-8 -*-
import re
import time

import requests


def get_one_page(url):
    header = {
        'authority': 'www.hasselblad.com',
        'method': 'GET',
        'path': '/data/dealers.json',
        'scheme': 'https',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'cookie': '_ga=GA1.2.1971942478.1585801294; _gid=GA1.2.1527436290.1585801294; hideCookies=true; localeRedirect=zh-cn; acw_tc=b683069e15858042155666188e7bcff222841152f174c9c7cf0e31a79b',
        'referer': 'https://www.hasselblad.com/zh-cn/dealers/?itm_campaign=locale&itm_medium=button',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            print(response.text)
        else:
            print("没有返回值")
    except requests.RequestException as e:
        print(e)



if __name__ == '__main__':
    url = 'https://www.hasselblad.com/data/dealers.json'
    get_one_page(url)
