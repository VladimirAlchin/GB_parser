from pymongo import MongoClient
from pprint import pprint
import les02.var01 as v
import json


def create_con():
    client = MongoClient('localhost', 27017)
    db = client['gb_parser']
    collection = db.hh
    return collection


def load_to_db(collection):
    collection.insert_many(json.loads(v.start()))


def vac(min_cost=0, max_cost=0):
    # вывод всех значений в коллекции
    if min_cost == max_cost and min_cost == 0:
        all_docs = create_con().find({})
        return all_docs
    # если ввели не правильную пару
    elif min_cost >= max_cost and min_cost != 0:
        return print('Вы ввели не правильную пару значений')
    # вывод значение с минимальной зарплатой больше или равной минимальной ставки
    elif min_cost >= max_cost and max_cost == 0:
        for i in create_con().find({'Зарплата_нижний_порог': {'gte': min_cost}}):
            pprint(i)
        return print('Вывод окончен')

    for i in create_con().find({'Зарплата_нижний_порог': {'gte': min_cost, 'lte': max_cost}}):
        pprint(i)


for i in create_con().find({'Зарплата_нижний_порог': {'$gte': 10000, '$lte': ''}}):
    pprint(i)

# for i in db.hh.find({"Зарплата_нижний_порог": {'$gt': 100000}}):
#     pprint(i)

# удаление всех элементов коллекции
# collection.delete_many({})
