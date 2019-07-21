# -*- coding: utf-8 -*-
import scrapy
from qsbk.items import QsbkItem


class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/']

    def parse(self, response):
        divs = response.xpath("//div[@id='content-left']/div")
        for div in divs:
            item = QsbkItem()
            item['author'] = author = div.xpath(".//h2/text()").get().strip()
            content = div.xpath(".//div[@class='content']//text()").getall()
            item['content'] = content = "".join(content).strip()
            number = div.xpath(".//a[@class='qiushi_comments']//text()").getall()
            item['number'] = number = "".join(number).strip()
            # item = {"author":author, "content":content, "number":number}
            yield item
