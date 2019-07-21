# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.response.html import HtmlResponse


class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/']

    def parse(self, response):
        print("="*20)
        divs = response.xpath("//div[@id='content-left']/div")
        for div in divs:
            author = div.xpath(".//h2/text()").get().strip()
            content = div.xpath(".//div[@class='content']//text()").getall()
            content = "".join(content).strip()
            number = div.xpath(".//a[@class='qiushi_comments']//text()").getall()
            number = "".join(number).strip()
            print(author)
            print(content)
            print(number)
        print("="*20)

