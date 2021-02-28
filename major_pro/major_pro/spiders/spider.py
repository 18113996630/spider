# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
import random
import time
import re


class SpiderSpider(CrawlSpider):
    name = 'spider'
    allowed_domains = ['https://www.bilibili.com/']
    start_urls = ['https://passport.bilibili.com/login']

    def login_bilibili(self):
        driver = webdriver.Chrome(executable_path=r'D:\chrome\Application\chromedriver.exe')
        # 窗口最大化
        driver.maximize_window()
        driver.get('https://passport.bilibili.com/login')
        time.sleep(10)
        # 收藏
        driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[3]/div[3]/ul/li[6]/a').click()
        if re.findall(r'确定', driver.page_source, re.S):
            # 弹框
            driver.find_element_by_xpath('//*[@id="page-fav"]/div[3]/div[2]/div/div[3]/a/span').click()
        time.sleep(random.randint(1, 3))
        # 专业收藏夹
        driver.find_element_by_xpath('//*[@id="fav-createdList-container"]/ul/li[1]/a').click()
        cookies = driver.get_cookies()  # Selenium为我们提供了get_cookies来获取登录cookies
        driver.close()  # 获取cookies便可以关闭浏览器
        # 然后的关键就是保存cookies，之后请求从文件中读取cookies就可以省去每次都要登录一次的
        # 当然可以把cookies返回回去，但是之后的每次请求都要先执行一次login没有发挥cookies的作用
        json_cookies = json.dumps(cookies)  # 通过json将cookies写入文件
        with open('cookies.json', 'w') as f:
            f.write(json_cookies)

    def start_requests(self):
        self.login_bilibili()
        with open('cookies.json', 'r', encoding='utf-8') as f:
            list_cookies = json.loads(f.read())  # 获取cookies
            # 把获取的cookies处理成dict类型
        cookies_dict = dict()
        for cookie in list_cookies:
            # 在保存成dict时，我们其实只要cookies中的name和value，而domain等其他都可以不要
            cookies_dict[cookie['name']] = cookie['value']
        print(cookies_dict)
        yield scrapy.Request()

    def parse(self, response):
        item = {}
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        return item
