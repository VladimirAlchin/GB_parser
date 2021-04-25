import json
import os
import time
from lxml import html
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# путь к ядру C:\Users\Vladi\Downloads\chromedriver_win32

load_dotenv()
url_hw = "https://vk.com/tokyofashion"
search_text = 'модель'
xpath_main = "//div[@id='page_search_posts']/div[contains(@id, 'post-')]"

driver = webdriver.Chrome(os.getenv('DRIVER_PATH_CHROME'))
driver.get(url_hw)
field_search = driver.find_element_by_class_name('ui_tab_search')

time.sleep(1)
field_search.click()

field_search_text = driver.find_element_by_class_name('ui_search_field')
time.sleep(4)
field_search_text.send_keys(search_text + Keys.ENTER)

items = driver.find_elements_by_xpath(xpath_main)

time.sleep(4)
driver.quit()

print(items)


print(1)