# -*- coding: UTF-8 -*-
import re
import time

import requests


def get_one_page(url):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'ASP.NET_SessionId=mnenpvswb1fgg2guu14izmn5; Ecp_ClientId=8200318221802137589; SID_kns=123123; SID_klogin=125141; Ecp_IpLoginFail=200318182.148.27.196; SID_kns_new=123114; KNS_SortType=; SID_crrs=125131; RsPerPage=20; SID_krsnew=125132; cnkiUserKey=386bbf09-3358-4be4-146c-6e10e023915c; _pk_ses=*; SID_kcms=124102; UM_distinctid=170ee03d2f654c-0b1831947d8b58-4313f6a-1fa400-170ee03d2f7547',
        'Host': 'kns.cnki.net',
        'Pragma': 'no-cache',
        'Referer': 'http://kns.cnki.net/kns/brief/default_result.aspx',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    params = {
        'pagename': 'ASP.brief_default_result_aspx',
        'isinEn': '1',
        'dbPrefix': 'SCDB',
        'dbCatalog': '中国学术文献网络出版总库',
        'ConfigFile': 'SCDBINDEX.xml',
        'research': 'off',
        't': str(int(time.time() * 1000)),
        'keyValue': '爬虫',
        'S': '1',
        'sorttype': ''
    }
    try:
        response = requests.get(url, headers=header, params=params)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.RequestException as e:
        print(e)


def parse_content(html):
    print('starting parse')
    regex = '<a class="fz14" href=.*target=\'_blank\'>(.*?)</a>'
    patten = re.compile(regex)
    items = re.findall(patten, html)
    idx = 0
    for item in items:
        print(idx, str(item).replace('<font class=Mark>', '').replace('</font>', ''))
        idx = idx + 1


if __name__ == '__main__':
    url = ' http://kns.cnki.net/kns/brief/brief.aspx'
    content = get_one_page(url)
    parse_content(content)
    print('解析结束')
