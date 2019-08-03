# -*- coding: utf-8 -*-
import scrapy
import json


class AgentSpiderSpider(scrapy.Spider):
    name = 'agent_spider'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/user-agent']

    def parse(self, response):
        print('='*50)
        print(json.loads(response.text)['user-agent'])
        # yield scrapy.Request(self.start_urls[0], dont_filter=True)
