# -*- coding: utf-8 -*-
import scrapy
import re


class FtxSpiderSpider(scrapy.Spider):
    name = 'ftx_spider'
    allowed_domains = ["fang.com"]
    start_urls = ["https://www.fang.com/SoufunFamily.htm"]

    def parse(self, response):
        trs = response.xpath("//*[@id='senfe']//tr")
        province = None
        for tr in trs:
            province_item = tr.xpath(".//td[not(@class)]")[0].xpath(".//text()").get()
            province_item = re.sub(r"\s", "", province_item)
            if province_item:
                province = province_item
            # 跳过海外
            if province == "其它":
                continue
            cities_info = tr.xpath(".//td[not(@class)]")[1].xpath(".//a")
            for city_info in cities_info:
                city_url = city_info.xpath(".//@href").get()
                city_name = city_info.xpath(".//text()").get()
                city_uri = city_url.split("//")[1].split(".")[0]
                if city_uri == "bj":
                    new_house_url = "https://newhouse.fang.com/house/s/"
                    stock_house_url = "https://esf.fang.com/"
                else:
                    new_house_url = "https://{}.newhouse.fang.com/house/s/".format(city_uri)
                    stock_house_url = "https://{}.esf.fang.com/".format(city_uri)
                yield scrapy.Request(url=new_house_url, callback=self.parse_new_house,
                                     meta={"info": (province, city_name)})
                yield scrapy.Request(url=stock_house_url, callback=self.parse_stock_house,
                                     meta={"info": (province, city_name)})
                break
            break

    def parse_new_house(self, response):
        province, city_name = response.meta.get("info")
        print(province, city_name)
        lis = response.xpath('//*[@id="newhouse_loupai_list"]/ul/li')
        for li in lis:
            name_info = li.xpath('.//div[contains(@class,"house_value")]/div[@class="nlcd_name"]/a')
            if not name_info:
                continue
            name = name_info.xpath('.//text()').get().strip()
            detail_url = response.urljoin(name_info.xpath('.//@href').get())
            house_type = li.xpath('.//div[contains(@class,"house_type")]/a/text()').getall()
            house_type = list(map(lambda x: re.sub(r"\s", "", x), house_type))
            print(name, detail_url, house_type)

    def parse_stock_house(self, response):
        pass
