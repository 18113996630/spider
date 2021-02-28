# -*- coding: utf-8 -*-
from pymysql import cursors
from twisted.enterprise import adbapi


class YuanrenxueSpiderPipeline(object):

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
        defer = self.dbpool.runInteraction(self.insert, item)
        defer.addErrback(self.hand_error, item, spider)
        return item

    def insert(self, cursor, item):
        self.sql = self.get_sql
        cursor.execute(self.sql,
                       (item['title'], item['author'], item['category'], item['time'], int(item['view_count']),
                        int(item['comment_count']), item['comment'], item['content'], item['detail_url']))

    def hand_error(self, error, item, spider):
        print('出现异常：{}，异常数据：{}'.format(error, item))

    @property
    def get_sql(self):
        if self.sql is None:
            self.sql = '''
                INSERT INTO `scrapy`.`yrx_mon`(`id`, `title`, `author`, `category`, `time`, `view_count`, 
                `comment_count`, `comment`, `content`, `detail_url`) 
                VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            '''
        return self.sql
