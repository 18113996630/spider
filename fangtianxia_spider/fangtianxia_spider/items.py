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
    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    location = scrapy.Field()
    price = scrapy.Field()
    house_type = scrapy.Field()
    for_sale = scrapy.Field()
    phone_num = scrapy.Field()
    size = scrapy.Field()
    detail_url = scrapy.Field()
    tag = scrapy.Field()
    # new ：标志该信息是新房信息
    type = scrapy.Field()
    page_url = scrapy.Field()


class StockHouseItem(scrapy.Item):
    """
    二手房
    """
    name = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    house_type = scrapy.Field()
    size = scrapy.Field()
    floor = scrapy.Field()
    orientation = scrapy.Field()
    build_year = scrapy.Field()
    owner = scrapy.Field()
    address = scrapy.Field()
    detail_url = scrapy.Field()
    total_price = scrapy.Field()
    avg_price = scrapy.Field()
    tag = scrapy.Field()
    village_name = scrapy.Field()
    # stock ：标志该信息是新房信息
    type = scrapy.Field()
    page_url = scrapy.Field()

