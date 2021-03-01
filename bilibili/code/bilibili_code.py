# -*- coding: UTF-8 -*-
import json
import os
import time
import random
from urllib import parse

import pandas as pd

import requests
import jsonpath
import pymysql.cursors
from selenium import webdriver
from fake_useragent import UserAgent

cookie_file_name = 'bilibili_cookies.json'
video_file_name = 'video.csv'
up_file_name = 'up.csv'

cookies_dict = dict()
zhuye_url = 'https://api.bilibili.com/x/space/acc/info?jsonp=jsonp&mid='
fensi_url = 'https://api.bilibili.com/x/relation/stat?jsonp=jsonp&vmid='
bofang_url = 'https://api.bilibili.com/x/space/upstat?jsonp=jsonp&mid='
video_list_url = 'https://api.bilibili.com/x/space/arc/search?ps=30&tid=0&pn=1&keyword=&order=stow&jsonp=jsonp&mid='
tag_url = 'https://api.bilibili.com/x/web-interface/view/detail/tag?aid='
comment_url = 'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=1&type=1&oid='
search_url = 'https://api.bilibili.com/x/web-interface/search/type?context=&page={page}&order=&keyword={keyword}&duration=&tids_1=&tids_2=&__refresh__=true&_extra=&search_type=video'

connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='bilibili',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()


def build_sql(table_name: str, item: dict, duplicate_fields: list):
    ls = [(k, v) for k, v in item.items() if v is not None]
    sql = 'INSERT INTO %s (' % table_name + ','.join([i[0] for i in ls]) + ') VALUES (' + ','.join(
        repr(i[1]) for i in ls) + ') ON DUPLICATE KEY UPDATE '
    for f in duplicate_fields:
        sql += '{f} = values ({f}),'.format(f=f)
    print(sql)
    return sql[:-1]


def save_data(sql: str):
    cursor.execute(sql)
    connection.commit()


def login():
    """
    第一次登陆则将cookie存起来，否则直接获取cookie
    :return:
    """
    if not os.path.exists(cookie_file_name):
        driver = webdriver.Chrome(executable_path=r'D:\chrome\chromedriver.exe')
        # 窗口最大化
        driver.maximize_window()
        driver.get("https://www.bilibili.com/")
        print('准备扫码登录,15秒后开始跳转页面')
        time.sleep(15)
        cookies = driver.get_cookies()
        json_cookies = json.dumps(cookies)  # 通过json将cookies写入文件
        with open(cookie_file_name, 'w') as f:
            f.write(json_cookies)
            print("cookie写入成功")
        driver.close()
    else:
        print("开始从cookie文件获取cookie")
        with open(cookie_file_name, 'r', encoding='utf-8') as f:
            list_cookies = json.loads(f.read())
        for cookie in list_cookies:
            cookies_dict[cookie['name']] = cookie['value']
        print("cookie获取成功")


def get_request_data(url):
    if '&_=' not in url:
        url += '&_=' + str(int(time.time() * 1000))
    header = {
        'user-agent': UserAgent().random
    }
    response = requests.get(url, cookies=cookies_dict, headers=header)
    while response.status_code != 200:
        get_request_data(url)
        time.sleep(random.randint(1, 10) / 10)
        if response.status_code == 200:
            return response.content.decode('utf-8')
    content = response.content.decode('utf-8')
    return content


def format_time(ts, style='%Y-%m-%d %H:%M:%S'):
    """
    格式化时间
    :param ts: 待格式化的时间
    :param style: 时间格式
    :return: 时间字符串
    """
    return time.strftime(style, time.localtime(ts))


def parse_video_data(video_url_inner: str, main_dic: dict):
    full_data = normalize_content(get_request_data(video_list_url + video_url_inner))
    # 总视频数量
    total_count = jsonpath.jsonpath(full_data, '$.data.page.count')[0]
    main_dic['spsl'] = total_count
    up_sql = build_sql('up_info', main_dic, ['fssl', 'spsl', 'ydl', 'dzl', 'bfl'])
    save_data(up_sql)

    # write_csv(main_dic, up_file_name)
    print('个人信息写入成功')
    cnt = 1
    for item in full_data['data']['list']['vlist']:
        single_video = dict()
        print('处理视频数量：', cnt)
        time.sleep(random.randint(1, 10) / 10)
        cnt += 1
        single_video['up_name'] = item['author']
        single_video['mid'] = item['mid']
        single_video['title'] = item['title']
        single_video['bfl'] = item['play']
        single_video['plsl'] = item['comment']
        single_video['dt'] = format_time(item['created'])
        single_video['length'] = item['length']
        single_video['dmsl'] = item['video_review']
        single_video['url'] = 'https://www.bilibili.com/video/' + item['bvid']
        # 获取tag数据
        single_video['tags'] = get_tags(tag_url + str(item['aid']))
        # 获取视频评论
        single_video['comments'] = get_comments(comment_url + str(item['aid']))
        save_data(build_sql('video', single_video, ['bfl', 'plsl', 'dmsl']))
        print('视频数据写入成功')


def get_comments(com: str):
    ds = normalize_content(get_request_data(com))
    comments = jsonpath.jsonpath(ds, '$.data.hots[0,1,2,].content.message')
    if comments:
        return '|'.join(comments)
    return ''


def get_tags(tag: str):
    ds = normalize_content(get_request_data(tag))
    tags = jsonpath.jsonpath(ds, '$.data[*].tag_name')
    if tags:
        return '|'.join(tags)
    return ''


def parse_main_info(mid: str):
    """
    处理个人相关的数据
    """
    zhuye = zhuye_url + mid
    json_data = normalize_content(get_request_data(zhuye))
    name = jsonpath.jsonpath(json_data, '$.data.name')[0]
    live_room_url = jsonpath.jsonpath(json_data, '$.data.live_room.url')[0]
    info = dict()
    info['url'] = 'https://space.bilibili.com/' + mid
    info['mid'] = mid
    info['name'] = name
    info['live_url'] = live_room_url
    """
    获取播放量等信息
    """
    d = normalize_content(get_request_data(bofang_url + mid))
    info['bfl'] = jsonpath.jsonpath(d, '$.data.archive.view')[0]
    info['ydl'] = jsonpath.jsonpath(d, '$.data.article.view')[0]
    info['dzl'] = jsonpath.jsonpath(d, '$.data.likes')[0]
    # 粉丝
    """
    获取粉丝信息
    """
    d = normalize_content(get_request_data(fensi_url + mid))
    info['fssl'] = jsonpath.jsonpath(d, '$.data.follower')[0]
    return info


def normalize_content(content: str):
    # 替换换行字符
    return json.loads(content.replace('\n', ';'))


def write_csv(data: dict, file_name):
    df = pd.DataFrame(data)
    if os.path.exists(file_name):
        df.to_csv(file_name, mode='a', header=False)
    else:
        df.to_csv(file_name, mode='a', header=True)


def imported(mid: int):
    up_sql = 'select count(1) as cnt from up_info where mid={mid}'.format(mid=mid)
    video_sql = 'select count(1) as cnt from up_info where mid={mid}'.format(mid=mid)
    cursor.execute(up_sql)
    up_cnt = cursor.fetchone()['cnt']
    cursor.execute(video_sql)
    video_cnt = cursor.fetchone()['cnt']
    print('当前mid为{mid}，up信息数量：{up}，视频数量：{video}'.format(mid=mid, up=up_cnt, video=video_cnt))
    return up_cnt >= 1 and video_cnt >= 1


def get_by_point_data():
    info = {
        '遇见狂神说': 95256449
    }
    for (name, mid) in info.items():
        # 获取个人信息
        print('current-user', name)
        main_dic = parse_main_info(str(mid))
        parse_video_data(str(mid), main_dic)


def get_by_keyword_search(code: str, max_page: int = 1):
    # 根据关键字搜索视频-
    # 分页查
    searched_ups = []
    for i in range(1, max_page + 1):
        ds = get_request_data(search_url.format(page=i, keyword=parse.quote(code)))
        js = normalize_content(ds)
        # 每页的数据
        for mid in jsonpath.jsonpath(js, '$.data.result[*].mid'):
            print('current user mid: {mid}'.format(mid=mid))
            if mid not in searched_ups:
                main_dic = parse_main_info(str(mid))
                parse_video_data(str(mid), main_dic)
                searched_ups.append(mid)
            else:
                print('the up has done')


if __name__ == '__main__':
    login()
    # get_by_point_data()
    keyword = 'java'
    max_page = 2
    get_by_keyword_search(keyword, max_page=max_page)
