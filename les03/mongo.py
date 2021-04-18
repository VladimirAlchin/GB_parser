from pymongo import MongoClient
from pprint import pprint
import les02.var01 as v
import json

client = MongoClient('localhost', 27017)
db = client['gb_parser']
collection = db.hh
collection.insert_many(json.loads(v.start()))
# for i in db.hh.find({"Зарплата_нижний_порог": {'$gt': 100000}}):
#     pprint(i)
# удаление всех элементов коллекции
# collection.delete_many({})
