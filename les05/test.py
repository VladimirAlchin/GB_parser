import json
import os
import time
from lxml import html
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs



a = open('f.txt', 'r', encoding='utf-8')
b = a.read()

soup = bs(b, "lxml")
item_list = soup.find_all("div", {"class": "_post"})
result_list = []
for i in item_list:
    post_text = i.find("div", {"class": "wall_post_text"})
    dir_post = {}
    if post_text != None:
        dir_post['post_text'] = post_text.text
        post_date = i.find("span", {"class": "rel_date"})
        if post_date != None:
            dir_post['post_date'] = post_date.text
        post_link = i.attrs
        dir_post['post_link'] = 'https://vk.com/wall' + post_link['data-post-id']

        photo_link = i.find("div", {"class": 'page_post_sized_thumbs'})
        photo_link_other ='https://vk.com/tokyofashion?z=photo'
        photo = []
        for j in photo_link.find_all('a'):
            try:
                photo.append(photo_link_other + j.attrs['data-photo-id'])
            except:
                break

        dir_post['photo_link'] = photo

        post_likes = i.find("a", {"class": "like"}).attrs['data-count']
        dir_post['post_likes'] = post_likes

        post_share = i.find("a", {"class": "share"}).attrs['data-count']
        dir_post['post_share'] = post_share

        post_views = i.find("div", {"class": "like_views _views"}).text
        dir_post['post_views'] = post_views
        result_list.append(dir_post)

def create_con():
    client = MongoClient('localhost', 27017)
    db = client['gb_parser']
    collection = db.post
    return collection


def load_data(col, data_list):
    col.insert_many(data_list)

load_data(create_con(), result_list)