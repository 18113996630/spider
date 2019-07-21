# -*- coding: UTF-8 -*-
from urllib.parse import urlencode

import requests
from config import *
from pyquery import PyQuery as pq

headers = {
    'Cookie': 'CXID=58C21F80D44BFE5AE732DB05C100C55E; SUID=DE83D1AB4C238B0A5AFAF07800087F7A; '
              'SUV=009E17847672AB325AFBB92DC377C978; ssuid=5028133892; SMYUV=1527931431877816; pgv_pvi=3597231104; '
              'wuid=AAHeKCvDJAAAAAqLEm8towoAGwY=; sw_uuid=9093734523; sg_uuid=6563246763; IPLOC=CN5101; '
              'ad=h42sBZllll2zMsxclllllVhttaUlllll$dpRTkllllwlllll4RqOnK@@@@@@@@@@; '
              'ld=6Zllllllll2toAu1lllllVhA3bylllllHIglBkllll9llllllylll5@@@@@@@@@@; '
              'SNUID=1D24C3FF4A4FCC495162682C4A40CE50; ABTEST=6|1554709855|v1; weixinIndexVisited=1; sct=4; '
              'JSESSIONID=aaaBaf45QKT2ddHpQKCNw; '
              'ppinf=5|1554710017|1555919617'
              '|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTklQkIlODQlRTglOEQlQTN8Y3J0OjEwOjE1NTQ3MTAwMTd8cmVmbmljazoxODolRTklQkIlODQlRTglOEQlQTN8dXNlcmlkOjQ0Om85dDJsdUpmXzJIWUNwY2xYM1otb2FxVmJxc0FAd2VpeGluLnNvaHUuY29tfA; pprdig=S0ULzagUptarV0mHYXERpHWV1rpGwFAR4B9yK7_ODioSqdtgFk1QqTBYQOuhFjeEKoA7Iv5C7h2nQkHIwK4qVMILPmXhnViNpdinaixbYcEdpFPENP8g3HasXj9Lhn0cXtlJKno6zrGV-8EI0cjayCSsAQvxZxcJCUa479UtjuE; sgid=13-39584835-AVyqicgFckJOmsjUfGtmDnNE; ppmdig=1554710017000000b2f66a10f48127e04ace6c4d9df65c8d',
    'Host': 'weixin.sogou.com',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

proxy = None


def get_proxy():
    """
    获取本地可用代理
    """
    try:
        global proxy
        _proxy = requests.get('http://127.0.0.1:5000/get')
        if _proxy.status_code == 200:
            proxy = {
                'http': 'http://' + _proxy.text
            }
            print('获取可用代理', proxy)
            return proxy
    except ConnectionError:
        return None


def get_html_by_page(page, count=1):
    """
    传入页数，获取搜狗html内容，当出现状态码为302时，调用get_proxy()获取可用代理
    """
    if count >= MAX_COUNT:
        print('重试超过{}次，无法获取第{}页内容'.format(MAX_COUNT, page))
        return None
    global proxy
    header = {
        'query': KEYWORD,
        'type': TYPE,
        'page': page,
        'ie': IE_VALUE
    }
    url = BASE_URL + urlencode(header)
    try:
        if proxy:
            # 当proxy有值的时候表示本机ip已经被封了，需使用代理ip
            html = requests.get(url, proxies=proxy, headers=headers, allow_redirects=False)
        else:
            html = requests.get(url, headers=headers, allow_redirects=False)
        if html.status_code == 200:
            return html.text
        if html.status_code == 302:
            # 获取代理进行请求
            print('the response code is 302')
            proxy = get_proxy()
            if proxy:
                count += 1
                get_html_by_page(page, count)
            else:
                print('none proxy available')
                return None
    except ConnectionError as e:
        get_proxy()
        count += 1
        print('请求异常:{}，开始第{}次重试'.format(e, count))
        get_html_by_page(page, count)


def get_article_urls_by_html(html):
    if html:
        doc = pq(html)


def main():
    # 传入页数获取html
    html = get_html_by_page(1)
    # 解析html，获取文章详情urls
    get_article_urls_by_html(html)


if __name__ == '__main__':
    main()
