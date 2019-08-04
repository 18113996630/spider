# -*- coding: utf-8 -*-

from scrapy.exporters import JsonLinesItemExporter


class WxappPipeline(object):

    def __init__(self) -> None:
        self.f = open('wx.json', 'wb')
        # 数据可能比较多，所以导入的是JsonLinesItemExporter，不会将数据存在内存中最后写入文件，而是爬取一条写入一条
        self.exporter = JsonLinesItemExporter(self.f, ensure_ascii=False, encoding="utf-8")

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self):
        self.f.close()
