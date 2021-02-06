# -*- coding: UTF-8 -*-
import re
import time

import requests


def get_one_page(url):
    data = {
        # 查看具体信息
        # 'urlName': 'CJFWZ_INFO',
        # 'id': 58190,
        # 查看地址
        # 'urlName': 'getAreaAllSubstation',
        # 信用社列表
        'urlName': 'CJFWZ_LIST',
        'pageSize': 10,
        'offset': 1,
        'unknown': 0,
        'e.name': '',
        'e.AccountX': '',
        'e.AccountY': ''
    }
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '86',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'areaCode=411681; cunId=57608; cunInfoBackId=3; validateimageName=a1b6e2ea-ca1c-4039-a9f2-c8ec2b1c13cc1586748298730',
        'Host': 'm.365960.cn',
        'Origin': 'https://m.365960.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://m.365960.cn/country_main.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        response = requests.post(url, headers=header, data=data)
        if response.status_code == 200:
            print(response.text)
        else:
            print("没有返回值")
    except requests.RequestException as e:
        print(e)



if __name__ == '__main__':
    url = 'https://m.365960.cn/ajaxHttp.do'
    get_one_page(url)
