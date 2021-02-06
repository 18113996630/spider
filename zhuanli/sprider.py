# -*- coding: UTF-8 -*-
import requests

url = 'https://www.letpub.com.cn/nsfcfund_search.php?mode=advanced&datakind=list&currentpage=1'
form_data = {
    'page': '',
    'name': '化学',
    'person': '',
    'no': '',
    'company': '',
    'addcomment_s1': '',
    'addcomment_s2': '',
    'addcomment_s3': '',
    'addcomment_s4': '',
    'money1': '',
    'money2': '',
    'startTime': '2019',
    'endTime': '2019',
    'subcategory': '',
    'searchsubmit': True,
}
response = requests.post(url, data=form_data)
if response.status_code == 200:
    print(response.content)

