# -*- coding: UTF-8 -*-

from selenium import webdriver
import random
import time
import re

urls = []


def parse(response, i):
    with open('html-{}'.format(i), "a", encoding='utf-8') as f:
        f.write(response)


driver = webdriver.Chrome(executable_path=r'D:\chrome\Application\chromedriver.exe')
# 窗口最大化
driver.maximize_window()
driver.get('https://passport.bilibili.com/login')
print('准备扫码登录,10秒后开始跳转页面')
time.sleep(10)
try:
    # 收藏
    driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[3]/div[3]/ul/li[6]/a').click()
    print('进入收藏界面')

    if re.findall(r'确定', driver.page_source, re.S):
        # 弹框
        print('发现弹框，7秒后继续运行')
        time.sleep(7)

    time.sleep(random.randint(3, 8))
    driver.refresh()
    print('进入大学专业收藏界面，准备分析界面')

    parse(driver.page_source, 1)
    time.sleep(random.randint(4, 9))
    for i in range(2, 13):
        driver.find_element_by_xpath('//*[@id="page-fav"]/div[1]/div[2]/div[3]/ul[2]/li[7]').click()
        print('开始查看第{}页数据'.format(i))
        parse(driver.page_source, i)
        time.sleep(random.randint(4, 9))
except Exception as e:
    print('出现异常，浏览器即将退出-{}'.format(e))
    driver.close()
