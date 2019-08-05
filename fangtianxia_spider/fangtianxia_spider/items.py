# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    """
    新房
    """
    name = scrapy.Field()
    location = scrapy.Field()
    price = scrapy.Field()
    house_type = scrapy.Field()
    for_sale = scrapy.Field()
    phone_num = scrapy.Field()
    size = scrapy.Field()
    detail_url = scrapy.Field()
    tag = scrapy.Field()


class StockHouseItem(scrapy.Item):
    """
    二手房
    """
    name = scrapy.Field()
    house_type = scrapy.Field()
    size = scrapy.Field()
    floor = scrapy.Field()
    orientation = scrapy.Field()
    build_year = scrapy.Field()
    owner = scrapy.Field()
    phone_num = scrapy.Field()
    location = scrapy.Field()
    detail_url = scrapy.Field()
    totle_price = scrapy.Field()
    avg_price = scrapy.Field()
    tag = scrapy.Field()
