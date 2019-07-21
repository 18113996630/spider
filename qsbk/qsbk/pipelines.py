# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class QsbkPipeline(object):

    def __init__(self):
        self.f = open("data.json", "w")

    def start_spider(self):
        print("爬虫已爬取到数据，开始保存")

    def close_spider(self):
        print("数据保存成功")
        self.f.close()

    def process_item(self, item, spider):
        item = json.dumps(dict(item), ensure_ascii=False)
        self.f.write(item + "\r\n")
