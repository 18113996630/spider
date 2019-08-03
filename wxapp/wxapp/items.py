# -*- coding: utf-8 -*-
import scrapy


class WxappItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    publish_time = scrapy.Field()
    content = scrapy.Field()
