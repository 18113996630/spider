# -*- coding: utf-8 -*-
import scrapy


class AgentSpiderSpider(scrapy.Spider):
    name = 'agent_spider'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/user-agent']

    def parse(self, response):
        print(response.text())
