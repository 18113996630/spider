# -*- coding: utf-8 -*-

import re

import scrapy

from fangtianxia_spider.items import NewHouseItem, StockHouseItem


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
                    continue
                else:
                    new_house_url = "https://{}.newhouse.fang.com/house/s/".format(city_uri)
                    stock_house_url = "https://{}.esf.fang.com/".format(city_uri)
                yield scrapy.Request(url=new_house_url, callback=self.parse_new_house,
                                     meta={
                                         "info": (province, city_name, new_house_url)
                                     })
                yield scrapy.Request(url=stock_house_url, callback=self.parse_stock_house,
                                     meta={
                                         "info": (province, city_name, stock_house_url),
                                     })

    def parse_new_house(self, response):
        """
        解析新房的页面数据
        :param response: response
        :return: 继续请求下一页
        """
        province, city_name, page_url = response.meta.get("info")
        lis = response.xpath('//*[@id="newhouse_loupai_list"]/ul/li')
        for li in lis:
            name_info = li.xpath('.//div[contains(@class,"house_value")]/div[@class="nlcd_name"]/a')
            if not name_info:
                continue
            name = name_info.xpath('.//text()').get().strip()
            detail_url = response.urljoin(name_info.xpath('.//@href').get())
            house_type = li.xpath('.//div[contains(@class,"house_type")]/a/text()').getall()
            house_type = " ".join(list(map(lambda x: re.sub(r"\s", "", x), house_type)))
            location = li.xpath('.//div[@class="nlc_details"]//div[@class="address"]/a/@title').get().strip()
            for_sale = li.xpath('.//div[contains(@class,"fangyuan")]/span/text()').get()
            price = "".join(
                li.xpath('.//div[@class="nlc_details"]//div[@class="nhouse_price"]//text()').getall()).strip()
            price = re.sub(r'\s|广告', '', price)
            tag = "-".join(li.xpath('.//div[@class="nlc_details"]//div[contains(@class,"fangyuan")]/a/text()').getall())
            phone_num = "".join(
                li.xpath('.//div[contains(@class,"relative_message")]/div[@class="tel"]/p//text()').getall())
            house_info = li.xpath('.//div[contains(@class,"house_type")]//text()').getall()
            house_info = re.sub(r'\s', '', "".join(house_info))
            size = re.findall('.+居.{1}(.*)', house_info)
            if size:
                size = size[0]
            else:
                size = '未知'
            item = NewHouseItem(province=province, city=city_name, name=name, location=location, price=price, tag=tag,
                         size=size, for_sale=for_sale, house_type=house_type, phone_num=phone_num,
                         detail_url=detail_url, type='new', page_url=page_url)
            yield item
        next_url = response.xpath('//li[@class="fr"]/a[last()-1]/@href').get()
        if next_url and 'https' not in next_url:
            next_url = response.urljoin(next_url)
        current_page_num = re.sub(r'\s', '', response.xpath('.//div[@class="page"]//a[@class="active"]/text()').get())
        print("第{}页的数据已爬取完毕，现在开始爬取下一页:{}".format(current_page_num, next_url))
        yield scrapy.Request(url=next_url, callback=self.parse_new_house, meta={
                                         "info": (province, city_name, next_url),
                                     })

    def parse_stock_house(self, response):
        """
        解析二手房的页面数据
        :param response: 请求相应体
        :return: 如果有下一页的话，就继续发送请求
        """
        province, city, page_url = response.meta.get("info")
        dls = response.xpath('//div[contains(@class,"shop_list")]/dl')
        for dl in dls:
            name = dl.xpath('.//h4/a/@title').get()
            infos = "".join(dl.xpath('.//p[@class="tel_shop"]//text()').getall())
            # 2室1厅|80㎡|中层（共6层）|南北向|蒋飞
            infos = re.sub(r'\s', '', infos)
            if len(infos.split('|')) >= 6:
                house_type = infos.split('|')[0]
                size = infos.split('|')[1]
                floor = infos.split('|')[2]
                orientation = infos.split('|')[3]
                build_year = infos.split('|')[4]
                owner = infos.split('|')[5]
                village_name = dl.xpath('.//p[@class="add_shop"]/a/@title').get()
                address = dl.xpath('.//p[@class="add_shop"]/span/text()').get()
                total_price = "".join(dl.xpath('.//dd[@class="price_right"]/span[1]//text()').getall())
                avg_price = dl.xpath('.//dd[@class="price_right"]/span[last()]/text()').get()
                feature = " ".join(dl.xpath('.//dd/p[last()]//text()').getall()).strip()
                feature = re.sub(r'\s', '', feature)
                detail_url = response.urljoin(dl.xpath('.//h4/a/@href').get())
                item = StockHouseItem(name=name, province=province, city=city, house_type=house_type, size=size, floor=floor,
                                     orientation=orientation, build_year=build_year, owner=owner, address=address,
                                     detail_url=detail_url, total_price=total_price, avg_price=avg_price, tag=feature,
                                     village_name=village_name, type='stock', page_url=page_url)
                yield item
        next_url = response.urljoin(response.xpath('.//div[@class="page_al"]/p[3]/a/@href').get())
        current_page_num = re.sub(r'\s', '', str(response.xpath('.//div[@class="page_al"]/span[@class="on"]/text()').get()))
        print("第{}页的数据已爬取完毕，现在开始爬取下一页:{}".format(current_page_num, next_url))
        yield scrapy.Request(url=next_url, callback=self.parse_stock_house, meta={
                                         "info": (province, city, next_url),
                                     })
