import datetime
from pprint import pprint
from lxml import html
import requests
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

url = 'https://yandex.com/news/'
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

# print(get_ya(url, headers))
