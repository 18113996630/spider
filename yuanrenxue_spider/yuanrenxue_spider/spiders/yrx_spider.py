# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from yuanrenxue_spider.items import YuanrenxueItem


class YrxSpiderSpider(CrawlSpider):
    name = 'yrx_spider'
    allowed_domains = ['yuanrenxue.com']
    start_urls = ['https://www.yuanrenxue.com/earn-money']

    rules = (
        Rule(LinkExtractor(allow=r'.+yuanrenxue.com/earn-money.+html'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        title = response.xpath('//h1[@class="title"]/a/text()').get()
        info = response.xpath('//div[@class="info"]')
        author = info.xpath('.//span[@class="author"]//text()').get()
        category = info.xpath('.//span[@class="list"]/a/text()').get()
        time = info.xpath('.//span[@class="time"]/text()').get()
        view_count = int("".join(re.findall(r'\d', info.xpath('.//span[@class="view"]/text()').get())))
        comment_count = int("".join(re.findall(r'\d', info.xpath('.//span[@class="cmt"]/text()').get())))
        comment = re.sub(r'\s', '', " | ".join(response.xpath('//li[contains(@class,"comment")]//text()').getall()))
        content = re.sub(r'\s', '', "".join(response.xpath('//div[@class="single-content"]//text()').getall()))
        detail_url = response.xpath('//h1[@class="title"]/a/@href').get()
        item = YuanrenxueItem(title=title, author=author, category=category, time=time, view_count=view_count,
                       comment_count=comment_count, comment=comment, content=content, detail_url=detail_url)
        yield item
