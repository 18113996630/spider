# -*- coding: utf-8 -*-

from pykafka import KafkaClient
from pymysql import cursors
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi


class MysqlPipeline(object):

    def __init__(self):
        db_params = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'scrapy',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        # self.cursor = pymysql.connect(**db_params).cursor()
        # 将db_params中的key作为参数中的key
        self.dbpool = adbapi.ConnectionPool("pymysql", **db_params)
        self.sql = None
        self.data = ()
        print("获取到数据库连接")

    def process_item(self, item, spider):
        self.sql = None
        defer = self.dbpool.runInteraction(self.insert_data, item)
        defer.addErrback(self.hand_error, item, spider)
        return item

    def close_spider(self, spider):
        print("爬虫结束")

    def insert_data(self, cursor, item):
        # 判断是新房还是二手房，调用不同的方法获取sql，处理好待插入的数据
        type = item['type']
        try:
            if type == 'new':
                self.sql = self.get_new_house_insert_sql
                self.data = (item['name'], item['province'], item['city'], item['location'], item['house_type'],
                             item['for_sale'], item['price'], item['size'], item['phone_num'], item['tag'],
                             item['page_url'])
                cursor.execute(self.sql, self.data)
            else:
                self.sql = self.get_stock_house_insert_sql
                self.data = (item['name'], item['province'], item['city'], item['house_type'], item['size'],
                             item['floor'], item['orientation'], item['build_year'], item['owner'],
                             item['address'], item['detail_url'], item['total_price'], item['avg_price'],
                             item['tag'], item['village_name'], item['page_url'])
                cursor.execute(self.sql, self.data)
        except Exception as e:
            print("异常：{} 出错的数据：{}".format(e, item))
            print("sql:", self.sql)
            print("data:", self.data)
            print("debugger")

    def hand_error(self, error, item, spider):
        print(error)
        print("出错的数据:{}".format(item))

    @property
    def get_new_house_insert_sql(self):
        if not self.sql:
            self.sql = """
               INSERT INTO `scrapy`.`new_house`(`id`, `name`,`province`, `city`,  `location`, 
                                           `house_type`, `for_sale`, `price`, 
                                           `size`, `phone_num`, `tag`, `page_url`) 
               VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               """
        return self.sql

    @property
    def get_stock_house_insert_sql(self):
        if not self.sql:
            self.sql = """
               INSERT INTO `scrapy`.`stock_house`(`id`, `name`, `province`, `city`, `house_type`, `size`, `floor`, `orientation`, 
               `build_year`, `owner`, `address`, `detail_url`, `total_price`, `avg_price`, `tag`, `village_name`, `page_url`) 
               VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               """
        return self.sql


class KafkaPipeline(object):
    """
    将爬取的数据写入kafka
    """

    def __init__(self):
        self.client = KafkaClient(hosts="n151:9092,n152:9092,n153:9092")
        self.topic = None
        self.producer = None

    def process_item(self, item, spider):
        type = item['type']
        if type == 'new':
            self.topic = self.client.topics['house_analysis.house.new']
        else:
            self.topic = self.client.topics['house_analysis.house.stock']
        self.producer = self.topic.get_producer()
        self.producer.produce(bytes(str(item), encoding='utf-8'))
