# -*- coding: utf-8 -*-
import scrapy


class FtxSpiderSpider(scrapy.Spider):
    name = 'ftx_spider'
    allowed_domains = ["fang.com"]
    start_urls = ["https://www.fang.com/SoufunFamily.htm"]

    def parse(self, response):
        trs = response.xpath("//table[@class='table01']/tr")
        for tr in trs:
            province = tr.xpath(".//td[not(@class)]")[1]
            city = tr.xpath(".//td[not(@class)]")[2]
            print(province)
            print(city)
            break
