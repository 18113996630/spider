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


def parse_video_data(content: str):
    full_data = normalize_content(content)
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

        title_list.append(title)
        play_count_list.append(play_count)
        comment_count_list.append(comment_count)
        dt_list.append(dt)
        length_list.append(length)
        danmu_list.append(danmu)
        url_list.append(url)
    data = dict()
    data['视频标题'] = title_list
    data['播放量'] = play_count_list
    data['评论数量'] = comment_count_list
    data['发布时间'] = dt_list
    data['视频长度'] = length_list
    data['弹幕数量'] = danmu_list
    data['视频地址'] = url_list
    write_csv_without_header(data, 'data.csv')


def parse_play_info(d: str):
    """
    获取播放量等信息
    """
    d = normalize_content(d)
    r = dict()
    r['video_view'] = jsonpath.jsonpath(d, '$.data.archive.view')[0]
    r['article_view'] = jsonpath.jsonpath(d, '$.data.article.view')[0]
    r['likes'] = jsonpath.jsonpath(d, '$.data.likes')[0]
    return r


def parse_fans_info(main_info: str):
    """
    获取粉丝信息
    """
    d = normalize_content(main_info)
    r = dict()
    r['fans'] = jsonpath.jsonpath(d, '$.data.follower')[0]
    return r


def parse_main_info(main_info: str):
    """
    处理个人相关的数据
    """
    json_data = normalize_content(main_info)
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
    content = content.replace('\n', ';')
    return json.loads(content)


def write_csv_without_header(data: dict, file_name):
    df = pd.DataFrame(data)
    df.to_csv(file_name, mode='a', header=False)


def write_csv_with_header(data, file_name):
    df = pd.DataFrame(data)
    df.to_csv(file_name, mode='a', header=True)


# login()
# content = '{"code":0,"message":"0","ttl":1,"data":{"list":{"tlist":{"160":{"tid":160,"count":23,"name":"生活"},"188":{"tid":188,"count":3,"name":"数码"},"217":{"tid":217,"count":3,"name":"动物圈"},"36":{"tid":36,"count":120,"name":"知识"}},"vlist":[{"comment":22,"typeid":122,"play":5958,"pic":"//i2.hdslb.com/bfs/archive/3c36ea50df68fd73081f6cbfec60e60bee90d411.jpg","subtitle":"","description":"https://www.youtube.com/watch?v=jA14r2ujQ7s\n0:00 - 简介\n0:28 - 第一章 仅仅是爱好\n1:08 - 第二章 死胡同？\n2:09 - 第三章 海投简历\n3:33 - 第四张 真正的工作\n4:11 -- 冒充者\n5:30 -- 学习编程最佳建议\n作者其他视频：BV1rV411U7BL","copyright":"","title":"【动画解读】没有计算机学位的如何自学编程并找到年薪百万工作？？","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1612403538,"length":"07:11","video_review":13,"aid":629032969,"bvid":"BV1et4y1B7Yp","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":171,"typeid":161,"play":4793,"pic":"//i1.hdslb.com/bfs/archive/4156aa15eecc29969b411ad9e8db67bab3d3641c.jpg","subtitle":"","description":"谁会是我的有缘人呢？","copyright":"","title":"【3D打印】礼物坐等有缘人","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1612148600,"length":"00:54","video_review":18,"aid":928905878,"bvid":"BV1WT4y1P7w2","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":51,"typeid":122,"play":29154,"pic":"//i2.hdslb.com/bfs/archive/ec63f33274785dc719c7ef07f156d43a44cb5483.jpg","subtitle":"","description":"https://www.youtube.com/watch?v=8RtGlWmXGhA\n乔治·霍兹（George Hotz，1989年10月2日－），美国学生，2007 年 8 月解锁苹果（Apple）iPhone手机。\n使得 iPhone 手机不仅仅局限于 AT\u0026T 网络，也支持其他 GSM 网络。\n2011年6月27日，黑客乔治·霍兹被曝加盟Facebook。","copyright":"","title":"学习编程的唯一方式【拳打苹果索尼脚踢特斯拉】","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1611972302,"length":"00:56","video_review":11,"aid":586401365,"bvid":"BV1cz4y1D7in","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":119,"typeid":161,"play":9010,"pic":"//i2.hdslb.com/bfs/archive/cb74f9cdbf2056894dad87b2315381d1755791da.jpg","subtitle":"","description":"耗时一周，反复调试，终于…………………","copyright":"","title":"耗时38小时为童鞋们准备“3D打印礼物”【邻居投诉｜反复失败｜猜对有奖】","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1611821108,"length":"00:51","video_review":12,"aid":246409198,"bvid":"BV1kv411s7eW","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":118,"typeid":222,"play":11616,"pic":"//i2.hdslb.com/bfs/archive/fec67bbd761b8fff6ba1054fa52b541d408848d9.jpg","subtitle":"","description":"小甲鱼？草龟？忍者？窄桥？圆奥？安布？剃刀？钻纹？猪鼻龟？蛋龟？黄喉？枯叶？巴西龟？地图？石金钱？火焰？鳄龟？麝香？黄缘？","copyright":"","title":"【小甲鱼？】办公室的龟龟们","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1611574325,"length":"01:04","video_review":87,"aid":501371339,"bvid":"BV1oN411d7XK","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":43,"typeid":122,"play":9727,"pic":"//i2.hdslb.com/bfs/archive/5b7a64b615de3d0ffa9fe8b089aa94ce773666fd.jpg","subtitle":"","description":"https://www.youtube.com/watch?v=ttcflCFd5B8\n不同类型的程序员/猿/媛\n偶遇大神：BV1BJ41157PJ","copyright":"","title":"不同类型的程序员【请对号入座】","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1611547420,"length":"04:16","video_review":55,"aid":713785966,"bvid":"BV13X4y1T7ko","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":479,"typeid":122,"play":11833,"pic":"//i2.hdslb.com/bfs/archive/0666dcadc3c70b7bb1dda6ce25a334fd1d7e293f.jpg","subtitle":"","description":"视频虽老，但理念不过时‍✿ヽ(°▽°)ノ✿\n想变强吗？除了坚持，还要选择一条最适合自己的编程路～\n请把“爷青回”打在弹幕上，谢谢～","copyright":"","title":"小甲鱼的学习路【弹指一挥间·听懂掌声】","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1611127239,"length":"18:07","video_review":332,"aid":798702775,"bvid":"BV18y4y1m7SZ","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":103,"typeid":122,"play":21769,"pic":"//i2.hdslb.com/bfs/archive/ff7e2e057e53b0fef93b0fb0f86a408c904187e7.jpg","subtitle":"","description":"使用了 checkra1n，linux-sandcastle，projectsandcastle 等开源项目\n同时自己编写了网桥设置 script/udev 规则来实现这一复杂的工作\n最终成功在这台坏掉的 iPhone7 上运行了 Ubuntu 20.04\n整个“服务器”系统都能够通过主服务器上的 USB 端口关闭电源","copyright":"","title":"16岁小哥硬核将废弃iPhone7移植为Linux服务器【膜拜】","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1610931604,"length":"04:53","video_review":26,"aid":843704178,"bvid":"BV1j54y1s7QH","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":18,"typeid":122,"play":7442,"pic":"//i1.hdslb.com/bfs/archive/38f54884407e458985061308d82e5b448536ff29.jpg","subtitle":"","description":"https://www.youtube.com/watch?v=oHtR5YSPLjo\n总结见置顶！\nPython教程：BV1Fs411A7HZ\nC语言教程：BV17s411N78s\nWeb教程：BV1QW411N762\n2021-TOP10编程语言：BV1U54y1W7y5","copyright":"","title":"2021给开发者的技术预测【未来已来？】","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1610772141,"length":"09:49","video_review":9,"aid":628655473,"bvid":"BV18t4y1z78P","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":96,"typeid":122,"play":12061,"pic":"//i0.hdslb.com/bfs/archive/667e9cf0b9706a8a1f034908843bf72d8b0c164e.jpg","subtitle":"","description":"视频虽老，但理念不过时‍✿ヽ(°▽°)ノ✿\n情怀，路遥知马力...\n请把“爷青回”打在弹幕上，谢谢～","copyright":"","title":"编程初学者的救赎【考古系列】","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1610620119,"length":"26:20","video_review":76,"aid":928713015,"bvid":"BV1LT4y1K7pn","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":72,"typeid":122,"play":11075,"pic":"//i2.hdslb.com/bfs/archive/f3837a6be13b4a20f62854e3bcecc3616323a2e0.jpg","subtitle":"","description":"变“废“为宝系列，不要“出戏”警告","copyright":"","title":"修复垃圾填埋场销毁旧 lphone12ProMax【万物皆可洗】","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1610509560,"length":"25:21","video_review":108,"aid":416186859,"bvid":"BV1DV411t7ES","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":192,"typeid":122,"play":31769,"pic":"//i0.hdslb.com/bfs/archive/4ad7e976fd5ad6c1120141f26108e92241e30124.jpg","subtitle":"","description":"https://www.youtube.com/watch?v=D7YMSt2ntWY\n排行榜：\n10. C#\n9. Go\n8. C++(BV1Ps411w73m)\n7. Javascript(BV1jE411T7ya)\n6.  Swift\n5. Java\n4. R Programming\n3. Kotlin\n2.  PHP\n1. Python(BV1Fs411A7HZ)","copyright":"","title":"2021年 10 大热门编程语言推荐","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1610242217,"length":"07:53","video_review":99,"aid":843582363,"bvid":"BV1U54y1W7y5","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":263,"typeid":122,"play":50884,"pic":"//i2.hdslb.com/bfs/archive/51c56f274a915372cdd14d41609341c5ef5c8f70.jpg","subtitle":"","description":"https://www.youtube.com/watch?v=jvg4VtYEhKU\nMinGW：https://bit.ly/mingw10\n官方 C 教程：BV17s411N78s","copyright":"","title":"在VSCode搭建C/C++环境【秒杀Visual C++/Dev C++]","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1609561144,"length":"09:09","video_review":56,"aid":628492673,"bvid":"BV1nt4y1r7Ez","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":16,"typeid":21,"play":3513,"pic":"//i2.hdslb.com/bfs/archive/d749c8bc4432688feb670e3add59a25076274e61.jpg","subtitle":"","description":"ilovefishc.com","copyright":"","title":"荣誉勋章有鱼C也有你们的一半【恭喜最后的3位锦鲤鱼油！！】","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1609490392,"length":"00:53","video_review":7,"aid":373379113,"bvid":"BV1xo4y1Z7yY","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":117,"typeid":122,"play":36071,"pic":"//i2.hdslb.com/bfs/archive/e7dfb728d32b2c3b2624dbfa2098225ca6656aed.jpg","subtitle":"","description":"https://www.youtube.com/watch?v=W--_EOzdTHk\nVSCode 最强 Python 环境搭建，知识点见置顶。\nPython 教程：BV1Fs411A7HZ\n快速解读版：BV1Qa4y1Y7vW\nKite 下载：https://www.kite.com/get-kite/","copyright":"","title":"在VSCode搭建Python环境【秒杀Pycharm？】","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1609315518,"length":"22:41","video_review":38,"aid":245757829,"bvid":"BV1yv41147rE","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":24,"typeid":21,"play":23820,"pic":"//i0.hdslb.com/bfs/archive/b0f33ea33df09574cab56e17acbe180ee38d2153.jpg","subtitle":"","description":"威胁性常规\n侮辱性极高\n‍","copyright":"","title":"这就是日常开发？？【威胁性常规||侮辱性极高】","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1609227142,"length":"00:53","video_review":23,"aid":203360239,"bvid":"BV1yh411f7gb","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":188,"typeid":122,"play":31820,"pic":"//i2.hdslb.com/bfs/archive/d25869ac6bd3178495232517cf2d0291e3b3d462.jpg","subtitle":"","description":"一款带你脱单的 VSCode 插件✿ヽ(°▽°)ノ✿","copyright":"","title":"一款带你脱单的 VSCode 的插件","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1608602109,"length":"17:03","video_review":208,"aid":500674954,"bvid":"BV1HK411G7iU","hide_click":false,"is_pay":0,"is_union_video":1,"is_steins_gate":0},{"comment":66,"typeid":21,"play":17885,"pic":"//i1.hdslb.com/bfs/archive/54f805392fc60dd6897fb4515ae02ac1aa55100a.jpg","subtitle":"","description":"沈阳一小区大门，居民通过 66 把锁接挂，打造“最便宜门禁系统”，这不就是“区块链”？？\n理由见视频[热词系列_知识增加]\n真实的比特币矿机：BV134411U7pB","copyright":"","title":"66把锁打造最便宜的“区块链”门禁？","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1608363989,"length":"00:11","video_review":7,"aid":458162592,"bvid":"BV1F5411V7CL","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":38,"typeid":122,"play":5545,"pic":"//i0.hdslb.com/bfs/archive/1c18577c10e6fbc720a71e3fcd1fca8886e4869c.jpg","subtitle":"","description":"https://www.youtube.com/watch?v=zQnBQ4tB3ZA\n微软官方JavaScript教程：BV18a4y1L7kD\n哈佛JavaScript：BV1dk4y117Yv\n速成课：BV1jE411T7ya","copyright":"","title":"100秒了解TypeScript【通俗易懂】","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1608102311,"length":"02:35","video_review":6,"aid":373178776,"bvid":"BV1DZ4y1g7H2","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":36,"typeid":122,"play":20367,"pic":"//i0.hdslb.com/bfs/archive/3333b114c84a0b99b136bbacce9bd77c1f314483.jpg","subtitle":"","description":"https://www.youtube.com/watch?v=c-I5S_zTwAc\n微软官方JavaScript教程：BV18a4y1L7kD\n哈佛JavaScript：BV1dk4y117Yv\n速成课：BV1jE411T7ya","copyright":"","title":"5分钟学习JavaScript【2020版-图解】","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1606960807,"length":"05:36","video_review":11,"aid":885429970,"bvid":"BV1NK4y177yU","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":45,"typeid":122,"play":18972,"pic":"//i0.hdslb.com/bfs/archive/eef24b5cc92aefbb8ebc563fb06107b79c993153.jpg","subtitle":"","description":"https://www.youtube.com/watch?v=QXjU9qTsYCc\n计算机是如何读懂你写的程序呢？？","copyright":"","title":"计算机如何读懂你写的程序？？【01000101000101】","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1606357495,"length":"12:08","video_review":65,"aid":500400200,"bvid":"BV1BK411V7SW","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":24,"typeid":201,"play":12359,"pic":"//i1.hdslb.com/bfs/archive/16138fef8da8e381f0027433d4fe040f47a890df.jpg","subtitle":"","description":"https://www.youtube.com/watch?v=F8_ME4VwTiw\n只要 5 步搭建最适合自己的办公桌位✿ヽ(°▽°)ノ✿！！","copyright":"","title":"【字幕组颈椎病十级患者强烈推荐】人体工程学家教你如何设置办公桌","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1605755050,"length":"03:39","video_review":13,"aid":712860761,"bvid":"BV1KD4y1X7cM","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":543,"typeid":21,"play":607688,"pic":"//i0.hdslb.com/bfs/archive/733da17ca7059af5c47cc633c9114953c0d79e6d.jpg","subtitle":"","description":"原来不止昙花会一现✧(≖ ◡ ≖✿)","copyright":"","title":"原来不止昙花会一现✧(≖ ◡ ≖✿)","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1605507449,"length":"00:31","video_review":7025,"aid":670282947,"bvid":"BV1Va4y1x7aK","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":73,"typeid":201,"play":42182,"pic":"//i1.hdslb.com/bfs/archive/709291e9f411c9ce9e006f46c8cb2625172877f7.jpg","subtitle":"","description":"https://www.youtube.com/watch?v=DWwlMOTgVJg\n对比1996年与2020年当前的情况，当年的蓝天白云绿地已经不见了，都被葡萄藤覆盖了，景色大不如前。\n不过这才是它本来的面目，当地原本就是葡萄种植地，奥瑞尔拍照的时候是休耕，之后很快就又种上了葡萄\n有兴趣的话，可以用谷歌地球寻找下这个地方，坐标为：38.248966, -122.410269","copyright":"","title":"Windows XP著名桌面20后大揭秘【结 局 唏 嘘...】","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1604452123,"length":"01:21","video_review":37,"aid":585140389,"bvid":"BV1kz4y1C7Qp","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":308,"typeid":122,"play":93975,"pic":"//i2.hdslb.com/bfs/archive/77ffc95b43398e1091013b6890304fd0288160a0.jpg","subtitle":"","description":"林纳斯·班奈狄克·托瓦兹（Linus Benedict Torvalds，1969年12月28日－），生于芬兰赫尔辛基市，拥有美国国籍，Linux内核的最早作者，随后发起了这个开源项目，担任Linux内核的首要架构师与项目协调者，是当今世界最著名的电脑程序员、黑客之一。\n他还发起了Git这个开源项目，并为主要的开发者。\nC 语言大神-\u003eBV1sE411D7hE","copyright":"","title":"Linus：没有比 C 更好的编程语言【Linux 创始人亲述】","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1604034810,"length":"01:44","video_review":86,"aid":330055104,"bvid":"BV1XA411L72R","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":42,"typeid":122,"play":19883,"pic":"//i2.hdslb.com/bfs/archive/8ca53b89e967a5b397a4f3aea101e9cd88c5b2b0.jpg","subtitle":"","description":"https://www.youtube.com/watch?v=BBwEF6WBUQs\n5年前基于 OpenCV+Python+Arduino 实现的自动驾驶\n相关课程：\nPython-\u003eBV1Fs411A7HZ\nOpenCV-\u003eBV1kJ41147s1\nC-\u003eBV17s411N78s","copyright":"","title":"【自动驾驶原型】基于OpenCV和Python实现自动驾驶","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1603246923,"length":"03:22","video_review":73,"aid":627545240,"bvid":"BV18t4y1i7jT","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":81,"typeid":122,"play":35035,"pic":"//i0.hdslb.com/bfs/archive/9a49176150941272b09c4ff40508cd9a3a93ccb7.jpg","subtitle":"","description":"https://channel9.msdn.com/Series/Beginners-Series-to-JavaScript/Beginning-the-Beginners-series-1-of-51\n在整个课程中，微软帮助用户使用 Visual StudioCode 设置开发环境，将 Node.js 安装为 JavaScript Runtime。\n在课程中提供了 JavaScript 的语法，并逐渐深入研究更高级的主题，包括对象和具有异步功能的编程，探索 JavaScript 生态系统以及","copyright":"","title":"微软最新推出的JavaScript实战教学【鱼C字幕组翻译中】","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1602812037,"length":"266:21","video_review":52,"aid":669993964,"bvid":"BV18a4y1L7kD","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":34,"typeid":124,"play":5941,"pic":"//i2.hdslb.com/bfs/archive/406d35df347d800a30f00e436e3c2ec185474edd.jpg","subtitle":"","description":"https://www.youtube.com/watch?v=zMua0cuhFnc\n人物介绍：\n小橘-\u003eServerless 无服务器\n小紫-\u003eAPI 网关\n小蓝-\u003eServerless MongoDB\n小红-\u003e事件中心","copyright":"","title":"云计算界中顶流Rap歌曲【你想成为rapstar吗】","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1602747043,"length":"06:11","video_review":16,"aid":329954714,"bvid":"BV1NA411E7wx","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":91,"typeid":122,"play":36039,"pic":"//i2.hdslb.com/bfs/archive/a3528318575fb42fcab10dd4cb7e583adfc804ee.jpg","subtitle":"","description":"https://www.youtube.com/watch?v=j48LtUkZRjU\nUnity 是由 Unity Technologies 研发的跨平台 2D/3D 游戏引擎，可用于开发 Windows、MacOS 及 Linux 平台的单机游戏，PlayStation、Xbox、Wii、任天堂 3DS 和 Switch 等游戏主机平台的视频游戏，以及 iOS、Android 等移动设备的游戏。","copyright":"","title":"如何制作一款电子游戏??","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1602495783,"length":"03:17","video_review":336,"aid":244951646,"bvid":"BV1vv411k7uy","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0},{"comment":43,"typeid":21,"play":8308,"pic":"//i1.hdslb.com/bfs/archive/c744100dd0c34567905ba9587edbed75127ffc12.jpg","subtitle":"","description":"天使 || 恶魔 之眼？？","copyright":"","title":"天使 || 恶魔 之眼？？","review":0,"author":"鱼C-小甲鱼","mid":314076440,"created":1600610272,"length":"00:33","video_review":4,"aid":457201696,"bvid":"BV1o5411L71L","hide_click":false,"is_pay":0,"is_union_video":0,"is_steins_gate":0}]},"page":{"pn":1,"ps":30,"count":149},"episodic_button":{"text":"播放全部","uri":"//www.bilibili.com/medialist/play/314076440?from=space"}}}'
# detail_url='https://api.bilibili.com/x/web-interface/view/detail/tag?aid=629032969'
# reply_url='https://api.bilibili.com/x/v2/reply?callback=jQuery17209811378174730223_1612621733781&jsonp=jsonp&pn=1&type=1&oid=671537082&sort=2&_=1612621734149'
# content = get_video_info(detail_url)
# print(content)
# parse_video_data(content)
content = '{"code":0,"message":"0","ttl":1,"data":{"mid":314076440,"name":"鱼C-小甲鱼","sex":"男","face":"http://i0.hdslb.com/bfs/face/4543ce186f9b74e60a85e66c010187bd3be3d0e1.jpg","sign":"让自学编程变得快乐有趣 ｡◕‿◕｡   ","rank":10000,"level":6,"jointime":0,"moral":0,"silence":0,"birthday":"05-20","coins":0,"fans_badge":true,"official":{"role":1,"title":"bilibili 知名科普UP主","desc":"","type":0},"vip":{"type":2,"status":1,"theme_type":0,"label":{"path":"","text":"年度大会员","label_theme":"annual_vip"},"avatar_subscript":1,"nickname_color":"#FB7299"},"pendant":{"pid":1141,"name":"如果历史是一群喵","image":"http://i2.hdslb.com/bfs/garb/item/cd3e9a6fa18db9ebdc128b0fef64cb32c5aab854.png","expire":0,"image_enhance":"http://i2.hdslb.com/bfs/garb/item/cd3e9a6fa18db9ebdc128b0fef64cb32c5aab854.png","image_enhance_frame":""},"nameplate":{"nid":1,"name":"黄金殿堂","image":"http://i2.hdslb.com/bfs/face/82896ff40fcb4e7c7259cb98056975830cb55695.png","image_small":"http://i1.hdslb.com/bfs/face/627e342851dfda6fe7380c2fa0cbd7fae2e61533.png","level":"稀有勋章","condition":"单个自制视频总播放数\u003e=100万"},"is_followed":false,"top_photo":"http://i2.hdslb.com/bfs/space/ca68c9c4c505d0fcb29d3377be57541ede5d1256.png","theme":{},"sys_notice":{},"live_room":{"roomStatus":1,"liveStatus":0,"url":"https://live.bilibili.com/10450003","title":"鱼C-小甲鱼的投稿视频","cover":"","online":28,"roomid":10450003,"roundStatus":1,"broadcast_type":0}}}'
data = parse_main_info(content)
write_csv_with_header(data, 'main.csv')