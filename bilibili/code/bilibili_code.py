# -*- coding: UTF-8 -*-
import json
import os
import time
import pandas as pd

import requests
import jsonpath
from selenium import webdriver

cookie_file_name = 'bilibili_cookies.json'
cookies_dict = dict()
zhuye_url = 'https://api.bilibili.com/x/space/acc/info?jsonp=jsonp&mid='
fensi_url = 'https://api.bilibili.com/x/relation/stat?jsonp=jsonp&vmid='
bofang_url = 'https://api.bilibili.com/x/space/upstat?jsonp=jsonp&mid='
video_list_url = 'https://api.bilibili.com/x/space/arc/search?ps=30&tid=0&pn=1&keyword=&order=stow&jsonp=jsonp&mid='
tag_url = 'https://api.bilibili.com/x/web-interface/view/detail/tag?aid='


def login():
    """
    第一次登陆则将cookie存起来，否则直接获取cookie
    :return:
    """
    if not os.path.exists(cookie_file_name):
        driver = webdriver.Chrome(executable_path=r'E:\chrome\chromedriver.exe')
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
    else:
        print("开始从cookie文件获取cookie")
        with open(cookie_file_name, 'r', encoding='utf-8') as f:
            list_cookies = json.loads(f.read())
        for cookie in list_cookies:
            cookies_dict[cookie['name']] = cookie['value']
        print("cookie获取成功")


def get_request_data(url):
    response = requests.get(url, cookies=cookies_dict)
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        return content
    return None


def format_time(ts, style='%Y-%m-%d %H:%M:%S'):
    """
    格式化时间
    :param ts: 待格式化的时间
    :param style: 时间格式
    :return: 时间字符串
    """
    return time.strftime(style, time.localtime(ts))


def parse_video_data(video_list: str):
    full_data = normalize_content(get_request_data(video_list))
    # 总视频数量
    total_count = jsonpath.jsonpath(full_data, '$.data.page.count')[0]
    # 每个视频的信息
    title_list = list()
    play_count_list = list()
    comment_count_list = list()
    dt_list = list()
    length_list = list()
    danmu_list = list()
    url_list = list()
    tag_list = list()
    cnt = 1
    for item in full_data['data']['list']['vlist']:
        print('处理视频数量：', cnt)
        cnt += 1
        title = item['title']
        play_count = item['play']
        comment_count = item['comment']
        dt = format_time(item['created'])
        length = item['length']
        danmu = item['video_review']
        url = 'https://www.bilibili.com/video/' + item['bvid']
        tag_url = 'https://api.bilibili.com/x/web-interface/view/detail/tag?aid=' + item['aid']
        tags = get_tags(get_request_data(tag_url))

        title_list.append(title)
        play_count_list.append(play_count)
        comment_count_list.append(comment_count)
        dt_list.append(dt)
        length_list.append(length)
        danmu_list.append(danmu)
        url_list.append(url)
        tag_list.append(tags)
    data = dict()
    data['视频标题'] = title_list
    data['播放量'] = play_count_list
    data['评论数量'] = comment_count_list
    data['发布时间'] = dt_list
    data['视频长度'] = length_list
    data['弹幕数量'] = danmu_list
    data['视频地址'] = url_list
    data['标签'] = tag_list
    write_csv_with_header(data, 'data.csv')


def get_tags(tag: str):
    ds = normalize_content(get_request_data(tag))
    return str(jsonpath.jsonpath(ds, '$.data[*].tag_name'))


def parse_play_info(bofang: str):
    """
    获取播放量等信息
    """
    d = normalize_content(get_request_data(bofang))
    r = dict()
    r['video_view'] = jsonpath.jsonpath(d, '$.data.archive.view')[0]
    r['article_view'] = jsonpath.jsonpath(d, '$.data.article.view')[0]
    r['likes'] = jsonpath.jsonpath(d, '$.data.likes')[0]
    return r


def parse_fans_info(fensi: str):
    """
    获取粉丝信息
    """
    d = normalize_content(get_request_data(fensi))
    r = dict()
    r['fans'] = jsonpath.jsonpath(d, '$.data.follower')[0]
    return r


def parse_main_info(zhuye: str):
    """
    处理个人相关的数据
    """
    json_data = normalize_content(get_request_data(zhuye))
    mid = jsonpath.jsonpath(json_data, '$.data.mid')
    name = jsonpath.jsonpath(json_data, '$.data.name')
    live_room_url = jsonpath.jsonpath(json_data, '$.data.live_room.url')

    info = dict()
    info['url'] = 'https://space.bilibili.com/' + str(mid[0])
    info['id'] = mid
    info['name'] = name
    info['live_room_url'] = live_room_url
    return info


def normalize_content(content: str):
    # 替换换行字符
    return json.loads(content.replace('\n', ';'))


def write_csv_without_header(data: dict, file_name):
    df = pd.DataFrame(data)
    df.to_csv(file_name, mode='a', header=False)


def write_csv_with_header(data, file_name):
    df = pd.DataFrame(data)
    df.to_csv(file_name, mode='a', header=True)


def parse():
    mid = 314076440
    video_url = video_list_url + str(mid)
    get_request_data(video_url)

login()
