# -*- coding: UTF-8 -*-
import scrapy


# 继承Spider类
class mingyan(scrapy.Spider):
    # 定义spider名字
    name = "mingyan"

    start_urls = [
        "http://lab.scrapyd.cn/page/1/",
        "http://lab.scrapyd.cn/page/2/"
    ]

    # def start_requests(self):
    #     urls = [
    #         "http://lab.scrapyd.cn/page/1/",
    #         "http://lab.scrapyd.cn/page/2/"
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        page = response.url.split('/')[-2]
        file_name = "mingyan-%s.html" % page
        with open(file_name, 'wb') as f:
            f.write(response.body)
        self.log("文件%s保存成功" % file_name)
