from bs4 import BeautifulSoup as bs
import requests as rs
import pickle
import json
import time


def variable():
    param = {
        'clusters': 'True',
        'area': '1',
        'ored_clusters': 'true',
        'enable_snippets': 'true',
        'salary': '',
        'st': 'searchVacancy',
        'text': 'python',
        'page': 0
    }
    url_search = 'https://hh.ru/search/vacancy?'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

    param['text'] = input(f'Введите искомую работу: ')
    max_page = int(input(f'Введите количество страниц для сбора от 1 до 40 : ')) - 1
    return url_search, headers, param, max_page


class GetHH:
    def __init__(self, name, url, header, param, max_page):
        self.param = param
        self.headers = header
        self.url_search = url
        self.answer = ''
        self.result = ''
        self.portal = name
        self.max_page = max_page

    def save_pickle(self, data):
        with open('hh.pcl', 'wb') as f:
            pickle.dump(data, f)

    def load_pickle(self):
        with open('hh.pcl', 'rb') as f:
            self.answer = pickle.load(f)
            return self.answer

    def get_data(self, url, header, param):
        self.answer = rs.get(url, headers=header, params=param)
        return self.answer

    def processing(self):
        self.get_data(self.url_search, self.headers, self.param)
        result_data = []
        while int(self.param['page']) <= self.max_page:
            soup = bs(self.answer.text, "html.parser")
            item_list = soup.find(attrs={"class": "vacancy-serp"})
            all_class = []
            for i in item_list.childGenerator():
                if len(i['class']) > 1:
                    for j in i['class']:
                        all_class.append(j)
                else:
                    all_class.append(i['class'][0])
            unique = []
            for i in sorted(set(all_class)):
                if 'vacancy' in i:
                    unique.append(i)
            items = soup.findAll(True, {'class': unique})
            for i in items:
                cost = i.find(attrs={"class": "vacancy-serp-item__sidebar"}).text.replace('\u202f', '').split(' ')
                if '–' in cost:
                    min_cost = cost[0]
                    max_cost = cost[2]
                    unit = cost[3]
                elif 'от' in cost:
                    min_cost = cost[1]
                    max_cost = 0
                    unit = cost[2]
                elif 'до' in cost:
                    min_cost = 0
                    max_cost = cost[1]
                    unit = cost[2]
                else:
                    min_cost = 0
                    max_cost = 0
                    unit = 0
                result_data.append(dict(zip(['id', 'Вакансия', 'Зарплата_нижний_порог', 'Зарплата_верхний_порог',
                                             'Валюта', 'Ссылка', 'Сайт'],
                                            [i.a["href"].split('/')[4], i.a.text, float(min_cost),
                                             float(max_cost), unit, i.a["href"], self.portal])))
            try:
                next_page = soup.find('a', {"data-qa": "pager-next"})['href']
                self.param['page'] += 1
                self.get_data(self.url_search, self.headers, self.param)
                time.sleep(0.5)
            except TypeError:
                break
        a = json.dumps(result_data, ensure_ascii=False, indent=2)
        self.result = a
        return a

    def save_data(self):
        with open('result.json', 'w', encoding='utf-8') as fa:
            fa.write(self.result)


def start():
    param = variable()
    my_hh = GetHH('хехе.ру', param[0], param[1], param[2], param[3])
    # для сохранения данных в файл расскоменировать эту строку
    # my_hh.save_data()
    return my_hh.processing()




