# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from novelspider.items import NovelspiderItem


class NSpiderSpider(CrawlSpider):
    name = 'n_spider'
    allowed_domains = ['kbiquge.com']
    start_urls = ['http://www.kbiquge.com/104_104216/28964754.html']

    rules = (
        Rule(LinkExtractor(allow=r'.+/104_104216/.+.html'), callback='parse_content', follow=False),
    )

    def parse_content(self, response):
        title = response.xpath('//h1/text()').get()
        content = "".join(response.xpath('//div[@id="content"]/text()').getall()).strip()
        print('='*40)
        print(title)
        print(content)
        print('='*40)
        yield NovelspiderItem(title=title, content=content)


