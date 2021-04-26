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
xpath_main = "//div[contains(@class,'_post ')]"

driver = webdriver.Chrome(os.getenv('DRIVER_PATH_CHROME'))
driver.get(url_hw)
field_search = driver.find_element_by_class_name('ui_tab_search')

time.sleep(1)
field_search.click()

field_search_text = driver.find_element_by_class_name('ui_search_field')
time.sleep(4)
field_search_text.send_keys(search_text + Keys.ENTER)

items = driver.page_source
print(len(items))
while True:
    time.sleep(2)
    try:
        button = driver.find_element_by_class_name('JoinForm__notNow')
        if button:
            button.click()
    finally:
        # b2 = driver.find_element_by_class_name('flat_button')
        # if b2:
        #     b2.click()
        field_search.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.25)
        field_search.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.25)
        field_search.send_keys(Keys.PAGE_DOWN)
        time.sleep(4)
        # if len(items) > len(driver.page_source):
        #     items = driver.page_source
        # else:
        #     break

print(len(items))
#
# with open('f.txt', 'w', encoding='utf-8') as f:
#     f.write(items)

time.sleep(4)
driver.quit()
