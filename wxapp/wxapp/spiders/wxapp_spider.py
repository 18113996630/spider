# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from wxapp.items import WxappItem


class WxappSpiderSpider(CrawlSpider):
    name = 'wxapp_spider'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']

    rules = (
        # follow=True表示会持续的爬取符合allow规则的url
        Rule(LinkExtractor(allow=r'.+mod=list&catid=2&page=\d'), follow=True),
        Rule(LinkExtractor(allow=r'.+article-.*\.html'), callback="parse_item", follow=False)
    )

    def parse_item(self, response):
        title = response.xpath('//*[@id="ct"]/div[1]/div/div[1]/div/div[2]/div[1]/h1/text()').get()
        author = response.xpath('//*[@id="ct"]/div[1]/div/div[1]/div/div[2]/div[3]/div[1]/p/a/text()').get()
        publish_time = response.xpath('//*[@id="ct"]/div[1]/div/div[1]/div/div[2]/div[3]/div[1]/p/span/text()').get()
        content = response.xpath('//*[@id="article_content"]//text()').getall()
        content = "".join(content).strip()
        print(title, author, publish_time, content)
        print('*'*30)
        item = WxappItem(title=title, author=author, publish_time=publish_time, content=content)
        yield item
