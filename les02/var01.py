from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests as rs
import pickle
import json
import time

# url_search = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post'
url_search = 'https://hh.ru/search/vacancy?clusters=true&area=1&ored_clusters=true&enable_snippets' \
             '=true&salary=&st=searchVacancy&text=python'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}


class GetHH:
    def __init__(self, name):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                      '(KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
        self.answer = ''
        self.result = ''
        self.portal = name

    def save_pickle(self, data):
        with open('hh.pcl', 'wb') as f:
            pickle.dump(data, f)

    def load_pickle(self):
        with open('hh.pcl', 'rb') as f:
            self.answer = pickle.load(f)
            return self.answer

    def get_data(self, url, header):
        self.answer = rs.get(url, headers=header)
        # self.save_pickle(self.answer.text)

    def processing(self):
        var_exit = 0
        result_data = []
        while 1 > 0:
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
                result_data.append(dict(zip(['Вакансия', 'Зарплата_нижний_порог', 'Зарплата_нижний_порог',
                                             'Валюта', 'Ссылка', 'Сайт'],
                                            [i.a.text, min_cost, max_cost, unit, i.a["href"], self.portal])))
            try:
                next_page = soup.find('a', {"data-qa": "pager-next"})['href']
                var_exit += 1
                txt = 'https://hh.ru' + next_page
                self.get_data(str(txt), self.headers)
                time.sleep(0.5)
            except TypeError:
                break
        a = json.dumps(result_data, ensure_ascii=False, indent=2)
        self.result = a
        return a

    def save_data(self):
        with open('result.json', 'w', encoding='utf-8') as fa:
            fa.write(self.result)


my_hh = GetHH('хехе.ру')
my_hh.get_data(url_search, headers)
my_hh.processing()
my_hh.save_data()


#     print(f'Вакансия {i.a.text} , ссылка {i.a["href"]}, минимум {min_cost} максимум {max_cost} валюта {unit}')
