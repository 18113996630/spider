# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class NSpiderSpider(CrawlSpider):
    name = 'n_spider'
    allowed_domains = ['kbiquge.com']
    start_urls = ['http://www.kbiquge.com/104_104216/28964754.html']

    rules = (
        Rule(LinkExtractor(allow=r'.+/104_104216/.+.html'), callback='parse_content', follow=True),
    )

    def parse_item(self, response):
        title = response.xpath('//h1/text()').get()
        content = "".join(response.xpath('//div[@id="content"]/text()').getall()).strip()


