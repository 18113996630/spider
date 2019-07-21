# -*- coding: UTF-8 -*-
import os
import re
import time

from pymysql import *
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

chrome = webdriver.Chrome()
chrome.get('https://www.taobao.com')
wait = WebDriverWait(chrome, 10)

today = time.strftime('%Y%m%d', time.localtime(time.time()))
table = "tb_data_" + today
file_path = 'E:/py_workspace/pc/taobao/data/'
sql = ''
keyword = '电脑'
file_name = "data_{}.txt_{}".format(keyword, today)
data_path = file_path + keyword + '/' + file_name


# 装饰器，计算插入50000条数据需要的时间
def timer(func):
    def decor(*args):
        start_time = time.time()
        func(*args)
        end_time = time.time()
        d_time = end_time - start_time
        print("the running time is : ", d_time)

    return decor


def parse_page():
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = chrome.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    products_dics = []
    for item in items:
        name = item.find('.title').text().replace("\n", '').replace('\r', '').replace('\t', '')
        price = item.find('.price').text().replace('¥\n', '')
        pay_count = item.find('.deal-cnt').text()[:-3]
        shop = item.find('.shop').text().replace("\n", '').replace('\r', '').replace('\t', '')
        location = item.find('.location').text().replace("\n", '').replace('\r', '').replace('\t', '')
        img_url = 'https:' + item.find('.pic .img').attr('src')

        product_dic = {
            'name': name,
            'price': price,
            'pay_count': pay_count,
            'shop': shop,
            'location': location,
            'img_url': img_url
        }
        products_dics.append(product_dic)
    return products_dics


def db_excute(sql):
    # local_infile = 1 执行load data infile
    db = connect("localhost", "root", "123456", "spider", local_infile=1)
    db.set_charset('utf8')
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except Error as e:
        print('err:{}'.format(e))
    finally:
        db.close()


# 导入infohash数据到mysql xl_log_analysis 表
def load_file(table):
    sql = "load data infile '{}' into table {} lines terminated by '\r\n' " \
          "(name,price,pay_count,shop,location,img_url)".format(
        data_path, table)
    print('sql:{}'.format(sql))
    db_excute(sql)


def load_search_page(keyword):
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
        search = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))
        )
        input.send_keys(keyword)
        search.click()
        print('请扫码登录淘宝')
        total_page = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total'))
        )
        print('登录成功')
        total_page = re.findall(re.compile('.*?(\d+).*?'), total_page.text)[0]
        print('总页数信息：{}'.format(total_page))
        print('开始解析第{}页的商品信息'.format(1))
        products_dics = parse_page()
        save_to_file(file_path, keyword, products_dics)
        return total_page
    except TimeoutException:
        print('超时，正在重试')
        load_search_page(keyword)


def go_next_page(page_number):
    try:
        print('开始解析第{}页的商品信息'.format(page_number))
        now_page = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        submit_btn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
        )
        now_page.clear()
        now_page.send_keys(page_number)
        submit_btn.click()
        next_page = wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active span'), str(page_number))
        )
        products_dics = parse_page()
        save_to_file(file_path, keyword, products_dics)
    except TimeoutException:
        print('第{}页加载超时，正在重试'.format(page_number))
        go_next_page(page_number)


def save_to_file(path, keyword, products):
    if not os.path.exists(path + '/' + keyword):
        os.mkdir(path + '/' + keyword)
    with open(data_path, 'a', encoding='utf-8') as f:
        for product in products:
            name = product.get('name')
            price = product.get('price')
            pay_count = product.get('pay_count')
            shop = product.get('shop')
            location = product.get('location')
            img_url = product.get('img_url')
            f.writelines('{}\t{}\t{}\t{}\t{}\t{}\n'.format(name, price, pay_count, shop, location, img_url))


@timer
def main():
    try:
        total_page = load_search_page(keyword)
        for i in range(2, int(total_page) + 1):
            go_next_page(i)
        load_file('data')
    except Exception:
        print('main方法出现异常')
        load_file('data')


if __name__ == '__main__':
    main()
