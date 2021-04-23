import datetime
import json
from pprint import pprint
from pymongo import MongoClient
from lxml import html
import requests
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

url_ya = 'https://yandex.com/news/'


def get_ya(url, headers):
    r = requests.get(url, headers=headers)
    r_html = html.fromstring(r.text)
    xpath_row = '//div[contains(@class, "news-top-flexible-stories")]/div'
    div_list = r_html.xpath(xpath_row)
    result_list = []
    for i in div_list:
        txt_h2 = './/h2/text()'
        url_news = './/a[@aria-label]//@href'
        source_text = './/span[contains(@class, "__source")]/a[contains(@aria-label, "Источник")]/text()'
        news_time = './/span[contains(@class, "mg-card-source__time")]/text()'
        dir_news = {}
        dir_news['create_at'] = datetime.datetime.now().isoformat()
        dir_news['url_search'] = url
        dir_news['text'] = i.xpath(txt_h2)[0].replace('\xa0', ' ')
        dir_news['url'] = i.xpath(url_news)[0]
        dir_news['news_id'] = dir_news['url'].split('=')[-1]
        dir_news['source'] = i.xpath(source_text)
        dir_news['time'] = i.xpath(news_time)[0]
        result_list.append(dir_news)
        time.sleep(1)
    return result_list


# print(get_ya(url_ya, headers))

url_mail = 'https://news.mail.ru/'


def get_mail(url, headers):
    r = requests.get(url_mail, headers=headers)
    r_html = html.fromstring(r.text)
    xpath_row = '//div[contains(@class, "daynews__item")]'
    div_list = r_html.xpath(xpath_row)
    result_list = []
    for i in div_list:
        txt_h2 = './/span[contains(@class, "photo__title")]/text()'
        url_news = './a/@href'
        source_text = './/a/span/text()'
        # не смог разобраться почему не работает xpath путь ниже в комментарии Для получения времени с новой страницы
        # news_time = '//span[@data-ago_content]/text()'
        news_time = '//span//@datetime'
        new_page = '//div[contains(@class, "breadcrumbs breadcrumbs_article js-ago-wrapper")]'
        dir_news = {}
        dir_news['create_at'] = datetime.datetime.now().isoformat()
        dir_news['url_search'] = url_mail
        dir_news['text'] = i.xpath(txt_h2)[0].replace('\xa0', ' ')
        dir_news['url'] = i.xpath(url_news)[0]
        dir_news['news_id'] = dir_news['url'].split('/')[-2]
        r_ = requests.get(dir_news['url'], headers=headers)
        r_html_ = html.fromstring(r_.text)
        new_list = r_html_.xpath(new_page)
        for j in new_list:
            dir_news['source'] = j.xpath(source_text)[0]
            dir_news['time'] = j.xpath(news_time)[0]
        result_list.append(dir_news)
        time.sleep(1)
    return result_list


url_lenta = 'https://lenta.ru/'


def get_lenta(url_lenta, headers):
    r = requests.get(url_lenta, headers=headers)
    r_html = html.fromstring(r.text)
    xpath_row = '//div[contains(@class, "b-yellow-box__wrap")]/div[contains(@class, "item")]'
    div_list = r_html.xpath(xpath_row)
    result_list = []
    for i in div_list:
        txt_h2 = './a/text()'
        url_news = './a/@href'
        news_time = '//time/@datetime'
        dir_news = {}
        dir_news['create_at'] = datetime.datetime.now().isoformat()
        dir_news['url_search'] = url_lenta
        dir_news['text'] = i.xpath(txt_h2)[0].replace('\xa0', ' ')
        dir_news['url'] = dir_news['url_search'] + i.xpath(url_news)[0]
        dir_news['news_id'] = i.xpath(url_news)[0]
        dir_news['source'] = 'lenta'
        dir_news['time'] = i.xpath(news_time)[0]
        time.sleep(1)
    return result_list


def create_con():
    client = MongoClient('localhost', 27017)
    db = client['gb_parser']
    collection = db.news
    return collection


def load_data(col, data_list):
    print(col)
    for i in data_list:
        print(i)


load_data(create_con(), get_ya(url_ya, headers))
