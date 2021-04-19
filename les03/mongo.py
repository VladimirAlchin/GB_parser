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
    # вывод значений без зп
    if min_cost == max_cost and min_cost == 0:
        print(1)
        for i in create_con().find({'Зарплата_нижний_порог': {'$eq': min_cost},
                                    'Зарплата_верхний_порог': {'$eq': max_cost}}):
            print(i)
        return print('Вывод окончен')
    # если ввели не правильную пару
    elif min_cost > max_cost and max_cost != 0:
        print(2)
        return print('Вы ввели не правильную пару значений')
    # вывод значение с минимальной зарплатой больше или равной минимальной ставки
    elif min_cost >= max_cost and max_cost == 0:
        print(3)
        for i in create_con().find({'Зарплата_нижний_порог': {'$gte': min_cost}}):
            pprint(i)
        return print('Вывод окончен')
    # вывод всех значений
    elif min_cost == -1:
        print(4)
        for i in create_con().find({}):
            print(i)
        return print('Вывод окончен')
    else:
        print(5)
        # вывод по условию больше или равно нижнему порогу и меньше или равно верхнему
        for i in create_con().find({'Зарплата_нижний_порог': {'$gte': min_cost}},
                                   {'Зарплата_верхний_порог': {'$lte': max_cost}},
                                   {'Зарплата_нижний_порог': {'$gt': 0}},
                                   {'Зарплата_верхний_порог': {'$gt': 0}}):
            print(i)
    return print('Вывод окончен')


vac(0, 45000)

# удаление всех элементов коллекции
# collection.delete_many({})
