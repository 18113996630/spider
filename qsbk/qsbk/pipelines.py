# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class QsbkPipeline(object):

    def __init__(self):
        self.f = open("data.json", "w", encoding="utf-8")

    def open_spider(self, spider):
        print("爬虫已爬取到数据，开始保存")

    def close_spider(self, spider):
        print("数据保存成功")
        self.f.close()

    def process_item(self, item, spider):
        data = json.dumps(dict(item), ensure_ascii=False)
        self.f.write(data + "\r\n")
        return item
