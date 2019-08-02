# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MspiderSpider(CrawlSpider):
    name = 'mspider'
    allowed_domains = ['www.taobao.com']
    start_urls = ['http://www.taobao.com/']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        return i
