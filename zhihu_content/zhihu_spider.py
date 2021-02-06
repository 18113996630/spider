# -*- coding: UTF-8 -*-
import json
import random
import time

import pymysql
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Major:

    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    id = 0
    name = ''


class Question:

    def __init__(self, url, question_title, question_description, answer_count) -> None:
        self.url = url
        self.question_title = question_title
        self.question_description = question_description
        self.answer_count = answer_count

    url = ''
    question_title = ''
    question_description = ''
    answer_count = 0


class Answer:
    def __init__(self, order_number, allow, up_count, author_name, author_desc, author_url, pub_time, content) -> None:
        self.order_number = order_number
        self.allow = allow
        self.up_count = up_count
        self.author_name = author_name
        self.author_desc = author_desc
        self.author_url = author_url
        self.pub_time = pub_time
        self.content = content

    order_number = 0
    allow = 1
    up_count = ''
    author_name = ''
    author_desc = ''
    author_url = ''
    pub_time = ''
    content = ''


suffix = ['专业怎么样', '专业就业怎么样', '专业前景怎么样', '专业好不好']
conn = pymysql.connect(
    host='localhost', user='root', passwd='123456', db='major_db', charset='utf8')
cur = conn.cursor()

# 打开浏览器开始搜索
driver = webdriver.Chrome(executable_path=r'D:\chrome\Application\chromedriver.exe')


def is_element_in_page(path, by_class=False):
    """
    根据xpath路径判断当前页面是否存在该元素
    :param xpath: xpath路径
    :return: 是否存在
    """
    try:
        if by_class:
            driver.find_element_by_class_name(path)
        else:
            driver.find_element_by_xpath(path)
        return True
    except Exception as _:
        return False


def read_cookies():
    """
    读取本地cookie
    :return:
    """
    print('开始读取cookie')
    driver.get("https://www.zhihu.com")
    with open("cookies.txt", "r") as fp:
        cookies = json.load(fp)
        for cookie in cookies:
            driver.add_cookie(cookie)


def search_by_keyword(keyword, index=1, search=True):
    """
    在主页根据关键字进行搜索
    :param keyword: 关键字
    :param index 点击第几个question
    :param search 是否根据关键词搜索
    :return: 页面跳转
    """
    if search:
        print('搜索关键词：{}'.format(keyword))
        input = driver.find_element_by_tag_name('input')
        input.send_keys(keyword)
        # 搜索
        input.send_keys(Keys.ENTER)
        time.sleep(random.randint(2, 6))
    # 定位帖子
    try:
        question_xpath = '//*[@id="SearchMain"]/div/div/div/div/div[{}]/div/div/h2/div/a'.format(index)
        driver.find_element_by_xpath(question_xpath).click()
    except BaseException as _:
        question_xpath = '//*[@id="SearchMain"]/div/div/div/div/div[{}]/div/div/h2/div/a'.format(index + 1)
        driver.find_element_by_xpath(question_xpath).click()
    print('点击第{}个搜索的帖子成功,成功跳转到回答详情页面并将driver切换到新页面'.format(index))
    handles = driver.window_handles
    for handle in handles:
        if handle != driver.current_window_handle:
            driver.switch_to.window(handle)
            break


def get_basic_info():
    """
    获取question基本信息
    :return: major_question
    """
    print('\t\t开始获取question数据...')
    url = driver.current_url
    # 问题title
    question_title = driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div[1]/div[2]/div[1]/div[1]/h1').text
    # 是否存在问题描述
    has_description = is_element_in_page('//*[@id="root"]/div/main/div/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/div')
    # 查看是否存在问题描述的更多按钮
    is_feasible = is_element_in_page(
        '//*[@id="root"]/div/main/div/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/div/button')
    question_description = ''
    if has_description:
        if is_feasible:
            # 点击显示更多，获取所有问题描述
            driver.find_element_by_xpath(
                '//*[@id="root"]/div/main/div/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/div/button').click()
            question_description = driver.find_element_by_xpath(
                '//*[@id="root"]/div/main/div/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/div/span').text
        else:
            # 直接获取问题描述
            question_description = driver.find_element_by_xpath(
                '//*[@id="root"]/div/main/div/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/div/span').text
    print('\t\tquestion数据获取完成...')
    return Question(url, question_title, question_description, 0)


def parse_question():
    """
    解析页面中的answer数据
    :return:
    """
    print('\t\t开始获取answer数据...')
    # 将评论展开
    driver.switch_to.window(driver.current_window_handle)
    time.sleep(random.randint(4, 7))
    has_more_content_btn = is_element_in_page('ContentItem-expandButton', by_class=True)
    answers = []
    try:
        driver.find_element_by_xpath(
            '//div[contains(@class, "Question-mainColumn")]//div[contains(@class, "ViewAll")]').click()
    except Exception as e:
        print('\t\t无查看所有')
    try:
        if has_more_content_btn:
            btn_flag = is_element_in_page('ContentItem-expandButton', by_class=True)
            if btn_flag:
                print('\t\t\t\t出现查看更多按钮...')
                btns = driver.find_elements_by_class_name('ContentItem-expandButton')
                for btn in btns:
                    script = "return arguments[0].scrollIntoView();"
                    driver.execute_script(script, btn)
                    btn.click()
                    time.sleep(random.randint(1, 2))
    except Exception as _:
        print('\t\t\t\t-')
    # 获取后续回答数据
    for i in range(random.randint(5, 9)):
        try:
            base_path = '//div[contains(@class, "AnswersNavWrapper") and contains(@class, "Card")]//div[@class="List-item"][{}]'.format(
                i + 1)
            if is_element_in_page(base_path + '//div[@class="AuthorInfo-head"]//a', by_class=False):
                author_name = driver.find_element_by_xpath(base_path + '//div[@class="AuthorInfo-head"]//a').text
                author_url = driver.find_element_by_xpath(base_path + '//div[@class="AuthorInfo-head"]//a').get_attribute(
                'href')
                author_desc = driver.find_element_by_xpath(base_path + '//div[@class="AuthorInfo-detail"]').text
            else:
                author_name = driver.find_element_by_xpath(base_path + '//div[@class="AuthorInfo-head"]//span').text
                author_url = ''
                author_desc = ''
            up_count = '0 人赞同了该回答'
            if is_element_in_page(base_path + '//div[@class="AnswerItem-extraInfo"]', by_class=False):
                up_count = driver.find_element_by_xpath(base_path + '//div[@class="AnswerItem-extraInfo"]').text
            content = driver.find_element_by_xpath(base_path + '//div[contains(@class, "RichContent-inner")]').text
            pub_time = driver.find_element_by_xpath(base_path + '//div[contains(@class, "ContentItem-time")]').text
            driver.find_element_by_xpath(base_path + '//button[contains(@class, "Button--iconOnly")]').click()
            time.sleep(0.4)
            text = driver.find_element_by_xpath('//div[contains(@class, "AnswerItem-selfMenu")]').text
            status = 1
            if '禁止转载' in text:
                status = 0
            driver.find_element_by_xpath(base_path + '//button[contains(@class, "Button--iconOnly")]').click()
            time.sleep(0.5)
            answers.append(Answer(1, status, up_count, author_name, author_desc, author_url, pub_time, content))
            offset = (i + 1) * 100
            driver.execute_script('document.documentElement.scrollTop={}'.format(offset))
        except BaseException as e:
            print('\t\t\t\t出现错误，开始抓取下一个回答:{}'.format(e.__cause__))
            continue
    return answers


def save_info_2_db(question, answers, major):
    """
    将数据存入mysql
    :param Question: 基本信息
    :param Answers: 回答数据
    :return: 保存是否成功
    """
    try:
        cur.execute('select count(1) from major_question where url= %s', [question.url])
        count = cur.fetchone()
        if int(count[0]) >= 1:
            print('该回答已爬取，跳过')
            return
        cur.execute(
            'INSERT INTO `major_db`.`major_question`( `url`, `major_id`, `major_name`, `title`, `description`, `answer_count`) '
            'VALUES ( %s, %s, %s, %s, %s, %s)',
            [question.url, major.id, major.name, question.question_title, question.question_description,
             len(answers)])
        cur.execute('select id from major_question where url = %s', [question.url])
        id = cur.fetchone()
        for answer in answers:
            cur.execute(
                'INSERT INTO `major_db`.`question_answer`(`author_name`, `author_url`, `author_description`, `time`, '
                '`content`, `order_number`, `major_question_id`, `up_count`, `allow`)'
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                [answer.author_name, answer.author_url, answer.author_desc
                    , answer.pub_time, answer.content, answer.order_number, id, answer.up_count, answer.allow])
        conn.commit()
        print('\t\t本次数据保存成功')
    except BaseException as e:
        print(e)
        print('【保存出错，将数据存入data.txt】')
        with open("data.txt", "a", encoding='utf-8') as f:
            for answer in answers:
                f.write('{}, {}, {}, {}, {}, {}'.format(question.url, major.id, major.name, question.question_title,
                                                        question.question_description,
                                                        len(answers)))
                f.write('\r\n')
                f.write('{}, {}, {}, {}, {}, {}, {}'.format(answer.author_name, answer.author_url, answer.author_desc
                                                            , answer.pub_time, answer.content, answer.order_number, 1))
                f.write('\r\n')


def save_info_2_db_second(question, answers):
    """
    将数据存入mysql
    :param Question: 基本信息
    :param Answers: 回答数据
    :return: 保存是否成功
    """
    try:
        cur.execute('select count(1) from major_question where url= %s', [question.url])
        count = cur.fetchone()
        if int(count[0]) >= 1:
            print('\t\t该回答已存在，开始更新数据')
            cur.execute('update `major_db`.`major_question` set `answer_count`= %s where url= %s ',
                [len(answers), question.url])
        cur.execute('select id from major_question where url = %s', [question.url])
        id = cur.fetchone()
        for answer in answers:
            cur.execute(
                'INSERT INTO `major_db`.`question_answer`(`author_name`, `author_url`, `author_description`, `time`, '
                '`content`, `order_number`, `major_question_id`, `up_count`, `allow`)'
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                [answer.author_name, answer.author_url, answer.author_desc
                    , answer.pub_time, answer.content, answer.order_number, id, answer.up_count, answer.allow])
        conn.commit()
        print('\t\t本次数据保存成功')
    except BaseException as e:
        print(e)
        print('【保存出错，将数据存入data.txt】')
        with open("data.txt", "a", encoding='utf-8') as f:
            for answer in answers:
                f.write('{}, {}, {}, {}, {}, {}'.format(question.url, major.id, major.name, question.question_title,
                                                        question.question_description,
                                                        len(answers)))
                f.write('\r\n')
                f.write('{}, {}, {}, {}, {}, {}, {}'.format(answer.author_name, answer.author_url, answer.author_desc
                                                            , answer.pub_time, answer.content, answer.order_number, 1))
                f.write('\r\n')


def get_major_info():
    """
    从数据库获取id，name数据
    :return:
    """
    cur.execute('select id, name from major')
    majors = []
    for item in cur.fetchall():
        majors.append(Major(item[0], item[1]))
    return majors


def return_last_page(name):
    """
    跳转回第一页
    :return:
    """
    print('跳转回主页')
    driver.close()
    driver.switch_to.window(name)
    input = driver.find_element_by_tag_name("input")
    input.clear()
    time.sleep(random.randint(2, 5))


def get_keys(major_name, current_name=None):
    if current_name is None:
        keys = major_name + random.choice(suffix)
    else:
        while True:
            keys = major_name + random.choice(suffix)
            if keys != current_name:
                break
    return keys


def is_searched(major):
    """
    判断是否已经爬取
    :param major: 专业
    :return: 判断结果
    """
    id = int(major.id)
    if id == 22:
        return True
    cur.execute('select count(1) from major_question where major_name= %s', [major.name])
    count = cur.fetchone()
    return int(count[0]) >= 3


def run():
    read_cookies()
    time.sleep(random.randint(2, 4))
    print('开始访问知乎首页')
    driver.get('https://www.zhihu.com')
    # 第一次使用时使用
    # print('准备登录,10秒后开始跳转页面')
    # time.sleep(10)
    # cookies = driver.get_cookies()
    # with open("cookies.txt", "w") as fp:
    #     json.dump(cookies, fp)
    # for name in majors:

    # 搜索条件拼接
    name = driver.current_window_handle
    print('当前window：{}'.format(name))
    majors = get_major_info()
    for major in majors:
        if is_searched(major):
            print('{}已经爬取过，跳过此次爬取'.format(major.name))
            continue
        keys = get_keys(major.name)
        search_by_keyword(keys, index=3)
        time.sleep(random.randint(2, 4))
        question = get_basic_info()
        answers = parse_question()
        print('\t\t保存第一个回答中的数据')
        save_info_2_db(question, answers, major)

        return_last_page(name)
        print('关闭当前页，爬取搜索结果中第二个回答的数据')
        search_by_keyword(keys, index=4, search=False)
        question_2 = get_basic_info()
        answer_2 = parse_question()
        save_info_2_db(question_2, answer_2, major)

        return_last_page(name)
        print('关闭当前页，开始搜索下一个关键词')
        driver.find_element_by_tag_name("input").clear()
        search_by_keyword(get_keys(major.name, keys), index=3)
        question_3 = get_basic_info()
        answer_3 = parse_question()
        save_info_2_db(question_3, answer_3, major)

        return_last_page(name)
        driver.find_element_by_tag_name("input").clear()
        print('开始进行下一个major的搜索')
    conn.close()
    cur.close()


def get_unfinished_source():
    cur.execute(
        'select id,url from major_question t where not exists(select 1 from question_answer m where m.major_question_id=t.id)')
    questions = []
    for item in cur.fetchall():
        questions.append(Major(item[0], item[1]))
    return questions


def run_add_info():
    read_cookies()
    time.sleep(random.randint(2, 4))
    questions = get_unfinished_source()
    print('开始访问剩余页面')
    for question in questions:
        # 加载页面
        driver.get(question.name)
        question = get_basic_info()
        answers = parse_question()
        print('\t\t保存回答中的数据')
        save_info_2_db_second(question, answers)
        print('开始进行下一个major的搜索')
    conn.close()
    cur.close()


if __name__ == '__main__':
    try:
        run_add_info()
    except Exception as e:
        while True:
            try:
                run_add_info()
            except Exception as e:
                run_add_info()
