# -*- coding: UTF-8 -*-
import requests
import time
import re

from fake_useragent import UserAgent

header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'intellpositionL=1522.39px; intellpositionT=655px; st_si=13296292195280; st_asi=delete; ASP.NET_SessionId=2qentta50fqoeqhhpuk2iwrb; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; EMFUND0=null; EMFUND8=02-28%2012%3A26%3A37@%23%24%u6C47%u6DFB%u5BCC%u4E2D%u8BC1%u73AF%u5883%u6CBB%u7406%u6307%u6570A@%23%24501030; EMFUND9=02-28 15:52:05@#$%u4EA4%u94F6%u4E2D%u8BC1%u73AF%u5883%u6CBB%u7406%28LOF%29@%23%24164908; qgqp_b_id=c2d37f4cfcabb8a3dbaf6a64a7c5d3c2; _qddaz=QD.dhyd6p.ikqeeq.klov00a6; st_pvi=44736027448903; st_sp=2021-01-24%2015%3A26%3A08; st_inirUrl=https%3A%2F%2Fwww.eastmoney.com%2F; st_sn=60; st_psi=20210228164656114-0-7039797475',
    'Host': 'fund.eastmoney.com',
    'Pragma': 'no-cache',
    'Referer': 'http://fund.eastmoney.com/data/fundranking.html',
    'User-Agent': UserAgent().random
}


def get(url):
    response = requests.get(url, headers=header)
    content = response.content.decode('UTF-8')
    print(content)
    return content


def parse_jijin_list(jijin_list_url):
    content = get(jijin_list_url)
    regex = '\"(.*?)\"'
    patten = re.compile(regex, re.S)
    for item in re.findall(patten, content):
        d = str(item).split(',')
        code = d[0]
        name = d[1]
        dt = d[3]
        dwjz = d[4]
        ljjz = d[5]
        rzzl = d[6]
        week = d[7]
        one_month = d[8]
        three_month = d[9]
        six_month = d[10]
        one_year = d[11]
        two_year = d[12]
        three_year = d[13]
        this_year = d[14]
        creat = d[15]
        sxf = d[20]
        print(code, name, dt, dwjz, ljjz, rzzl, week, one_month, three_month, six_month, one_year, two_year
              , three_year, this_year, creat, sxf)


if __name__ == '__main__':
    list_url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=gp&rs=&gs=0&sc=6yzf&st=desc&sd=2020-02-28&ed=2021-02-28&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.8662016657528548'
    parse_jijin_list(list_url)
# 获取持仓股票
# https://push2.eastmoney.com/api/qt/ulist.np/get?cb=jQuery18303261244154687355_1614502056083&fltt=2&invt=2&ut=267f9ad526dbe6b0262ab19316f5a25b&fields=f3,f12,f14&secids=1.603799,0.002460,0.300750,1.601633,0.002756,0.002240,0.002709,0.002407,0.002497,0.300073&_=1614502056519

# 相关个股
# http://push2.eastmoney.com/api/qt/slist/get?pi=0&pz=5&po=1&spt=4&fields=f2,f12,f13,f14,f15,f3,f4,f6,f5,f11,f10&ut=fa5fd1943c7b386f172d6893dbfba10b&secid=1.603799&fid=f3&cb=jQuery11240024976681334842432_1614502503509&_=1614502503510
# http://push2.eastmoney.com/api/qt/slist/get?pi=0&pz=5&po=1&spt=4&fields=f2,f12,f13,f14,f2,f3,f4,f6,f5,f11,f10&ut=fa5fd1943c7b386f172d6893dbfba10b&secid=1.603799&fid=f3&cb=jQuery11240024976681334842432_1614502503511&_=1614502503512

# 相关个股领涨股
# http://push2.eastmoney.com/api/qt/slist/get?ut=fa5fd1943c7b386f172d6893dbfba10b&spt=3&pi=0&pz=5&po=1&fields=f14,f3,f128,f12,f13,f100,f102,f103&secid=1.603799&cb=jQuery11240024976681334842432_1614502503525&_=1614502503526

# 个股—机构增持
# http://reportapi.eastmoney.com/report/list?beginTime=2019-02-28&endTime=2021-02-28&fields=orgCode,orgSName,sRatingName,encodeUrl,title,publishDate,market&pageNo=1&pageSize=5&qType=0&code=603799&cb=callback1088046&_=1614502503523
# http://reportapi.eastmoney.com/report/list?beginTime=2019-02-28&endTime=2021-02-28&fields=orgCode,orgSName,sRatingName,encodeUrl,title,publishDate&pageNo=1&pageSize=5&qType=1&industryCode=478&cb=callback115674&_=1614502985194
# 行业—机构看法
# http://reportapi.eastmoney.com/report/list?beginTime=2019-02-28&endTime=2021-02-28&fields=orgCode,orgSName,sRatingName,encodeUrl,title,publishDate&pageNo=1&pageSize=5&qType=1&industryCode=478&cb=callback4419505&_=1614502503524

# 相关文章看法
# http://cmsdataapi.eastmoney.com/api/organization/GetOrganizationArticleByIds?channelIds=9&pageIndex=1&pageSize=5&cb=jQuery11240024976681334842432_1614502503531&_=1614502503532
