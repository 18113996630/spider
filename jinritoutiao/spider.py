# -*- coding: UTF-8 -*-
import json
import os
import random
import re
import time
import pymongo
import requests

from bs4 import BeautifulSoup
from urllib3.connection import log
from _md5 import md5
from multiprocessing.pool import Pool
from urllib.parse import urlencode

from mongo_conf import *

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def request(url, type='text', headers=None, printOrNot=False):
    if headers:
        url = url + urlencode(headers)
    try:
        if printOrNot:
            print('开始请求:{}'.format(url))
        response = requests.get(url)
        if response.status_code == 200:
            if type == 'text':
                return response.text
            elif type == 'content':
                return response.content
        else:
            log.error('请求失败，请求状态码：{}', response.status_code)
            return None
    except requests.RequestException as e:
        log.error('请求出现异常，msg:{}', e.strerror)
        return None


def get_content_by_offset_and_keywords(offset, keyword):
    base_url = 'https://www.toutiao.com/api/search/content/?'
    header = {
        'aid': random.randint(1, 1000),
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'en_qc': 1,
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': time.time()
    }
    return request(base_url, headers=header, printOrNot=True)


def get_urls_by_html(html):
    """
    获取帖子详情链接
    """
    data = json.loads(html)
    urls = []
    if data and 'data' in data.keys():
        for item in data.get('data'):
            article_url = item.get('article_url')
            if article_url:
                urls.append(article_url)
        return urls


def download_image(title, urls):
    print('开始下载标题为{}下的{}张图片'.format(title, len(urls)))
    for url in urls:
        content = request(url, type='content')
        directory = '{}/{}'.format(os.getcwd(), title)
        if not os.path.exists(directory):
            os.mkdir(directory)
        path = '{}/{}/{}.{}'.format(os.getcwd(), title, md5(content).hexdigest(), 'jpg')
        with open(path, 'wb') as f:
            f.write(content)
            print('正在下载：{}'.format(url))


def save_to_mongo(info):
    if db[MONGO_TABLE].insert_one(info):
        print('保存到mongodb成功:{}'.format(info.get('title')))
    else:
        log.error('保存失败')


def parse_url(url):
    base_url = 'https://www.toutiao.com/a'
    patten = re.compile('http://toutiao.com/group/(.*?/)')
    id = re.findall(patten, url)
    if id:
        return base_url + id[0]
    return None


def parse_article_detail(url):
    """
    解析article的内容
    """
    html = request(url)
    if html:
        soup = BeautifulSoup(html, 'lxml')
        try:
            if 'galleryInfo' in soup.text:
                info_patten = re.compile('.*?galleryInfo = {(.*?)}var.*?', re.S)
            else:
                info_patten = re.compile('.*?articleInfo: {(.*?)},\n    commentInfo:.*?', re.S)
            articleInfo = re.findall(info_patten, soup.text)
            if len(articleInfo) == 1:
                title = re.findall(re.compile(".*?title.*?'(.*?)'.*?"), json.dumps(articleInfo[0], ensure_ascii=False))
                time = re.findall(re.compile(".*?time.*?'(.*?)'.*?"), json.dumps(articleInfo[0], ensure_ascii=False))

                url_patten = re.compile('.*?(http.*?)[&;"].*?')
                image_urls = re.findall(url_patten, str(soup.text))
                urls = []
                for image_url in image_urls:
                    urls.append(image_url.replace('\\', ''))
                return {
                    'title': title[0],
                    'time': time[0],
                    'image_count': len(image_urls),
                    'image_urls': urls
                }
            return None
        except requests.RequestException:
            return None
    return None


def main(offset, keyword='街拍图片'):
    html = get_content_by_offset_and_keywords(offset, keyword)
    urls = get_urls_by_html(html)
    print('解析完毕，offset为{}下网页共有{}条url'.format(offset, len(urls)))
    for i in range(len(urls)):
        url = parse_url(urls[i])
        count = i
        print('开始解析第{}条url:{}'.format(count + 1, url))
        infos = parse_article_detail(url)
        if infos:
            save_to_mongo(infos)
            download_image(infos.get('title'), infos.get('image_urls'))


if __name__ == '__main__':
    # 指定cpu个数
    pool = Pool(6)
    pool.map(main, [i for i in range(0, 41, 20)])
