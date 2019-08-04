# -*- coding: utf-8 -*-
import scrapy
from qsbk.items import QsbkItem


class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/']
    base_domain = "https://www.qiushibaike.com"

    def parse(self, response):
        divs = response.xpath("//div[@id='content-left']/div")
        for div in divs:
            item = QsbkItem()
            item['author'] = author = div.xpath(".//h2/text()").get().strip()
            content = div.xpath(".//div[@class='content']//text()").getall()
            item['content'] = content = "".join(content).strip()
            number = div.xpath(".//a[@class='qiushi_comments']//text()").getall()
            item['number'] = number = "".join(number).strip()
            yield item
        next_url = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        self.log("开始请求下一页数据")
        if not next_url:
            return
        else:
            yield scrapy.Request(self.base_domain+next_url, callback=self.parse)
