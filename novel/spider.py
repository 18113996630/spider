# -*- coding: UTF-8 -*-
import os
import time
import requests
import re
from pyquery import PyQuery as pq

base_url = 'https://m.biquke.com'
start_index = '/bq/3/3322/12536875.html'
start_url = 'https://m.biquke.com/bq/3/3322/12536875.html'
file_path = os.getcwd() + '\\data'
spider_count = 100


def get_html(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            # 将相应体进行正确编码
            response.encoding = response.apparent_encoding
            print('成功爬取url：{}'.format(url))
            return response.text
    except requests.RequestException as e:
        cnt = 1
        while cnt <= 3:
            print('爬取{} 出错:{} 开始重试第{}次'.format(url, e.strerror, cnt))
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                # 将响应体进行正确编码
                response.encoding = response.apparent_encoding
                print('成功爬取url：{}'.format(url))
                return response.text
        return None


def parse_save_html(html):
    try:
        print('开始解析。。。。')
        doc = pq(html)
        header = doc('#header > div.zhong').text()
        content = doc('#nr').text()
        next_url = doc('#zj > section.zj > div:nth-child(3) > a:nth-child(3)').attr('href')
        datas = {"success": True, "header": header, "content": content, "next_url": base_url + next_url}
        save_to_file(datas)
        print('解析完毕，该章标题为{}, 开始保存至本地。。。'.format(header))
        return datas
    except Exception as e:
        print('解析或保存过程出错，程序即将终止。。。')
        return {"success": False, "header": None, "content": '获取内容失败，请手动获取:{}'.format(e.__cause__), "next_url": None}


def save_to_file(datas):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(file_path + '\\zjnx.txt', 'a', encoding='utf-8') as f:
        f.writelines('{}\r\n{}\r\n'.format(datas.get('header'), datas.get('content')))


def get_last_url():
    start_index_num = start_index.split('/')[4].split('.')[0]
    last_index_num = int(start_index.split('/')[4].split('.')[0]) + spider_count
    last_index = start_index.replace(start_index_num, str(last_index_num))
    return base_url + last_index


def start(wait=1):
    cnt = 2
    html = get_html(start_url)
    datas = parse_save_html(html)
    while datas.get('success') and cnt <= spider_count:
        html = get_html(datas.get('next_url'))
        datas = parse_save_html(html)
        cnt += 1
        time.sleep(wait)
    if cnt >= spider_count:
        print('爬取完毕')
    else:
        print('爬取url{}过程中遇到错误，程序终止'.format(datas.get('next_url')))


if __name__ == '__main__':
    start(wait=0)


