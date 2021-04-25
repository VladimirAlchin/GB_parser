from bs4 import BeautifulSoup as bs
import lxml.html
import requests as rs
import pickle
import json
import time

a = open('f.txt', 'r', encoding='utf-8')
b = a.read()

soup = bs(b, "lxml")
item_list = soup.find_all("div", {"class": "_post"})
for i in item_list:
    post_text = i.find("div", {"class": "wall_post_text"})
    if post_text != None:
        print(post_text.text)
        post_date = i.find("span", {"class": "rel_date"})
        if post_date != None:
            print(post_date.text)
    # post_link = ''
    # post_link_image = []
    # post_like = ''
    # post_repost = ''
    # post_view = ''
