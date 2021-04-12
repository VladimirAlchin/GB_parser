from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests as rs
import pickle
import json
import time

url_hh = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}


class GetHH():
    def __init__(self):
        self.answer = ''

    def save_pickle(self, data):
        with open('hh.pcl', 'wb') as f:
            pickle.dump(data, f)

    def load_pickle(self):
        with open('hh.pcl', 'rb') as f:
            self.answer = pickle.load(f)
            return self.answer

    def get_data(self, url, header):
        self.answer = rs.get(url, headers=header)
        self.save_pickle(self.answer.text)

    def processing(self):
        soup = bs(self.answer, "html.parser")
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
        return items

    def save_data(self):
        pass


my_hh = GetHH()
my_hh.load_pickle()
# print(my_hh.processing())
for i in my_hh.processing():
    if len(i.find(attrs={"class": "vacancy-serp-item__sidebar"}).text) == 0:
        cost = 0
    else:
        cost = i.find(attrs={"class": "vacancy-serp-item__sidebar"}).text
    print(f'Вакансия {i.a.text} , ссылка {i.a["href"]}, зп {cost}')




