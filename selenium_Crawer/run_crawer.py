#coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains #引入ActionChains鼠标操作类
from selenium.webdriver.common.keys import Keys #引入keys类操作
import time
import random
import json

chrome_driver_path = './chromedriver'
home_page = 'http://drugs.dxy.cn'
save_file = 'sub_class_file.txt'
data_per = {}
start_ = 3
end_ = 16

browser = webdriver.Chrome(chrome_driver_path)
browser.get(home_page)

#click more hidden content


check_list = browser.find_element_by_class_name('sidemenu')
cli = check_list.find_element_by_class_name('more')
cli.click()
check_list = check_list.find_element_by_tag_name('ul')
check_list = check_list.find_elements_by_tag_name('li')

for i in check_list:
    sup_class = i.text.encode("utf-8").decode("utf-8")
    data_per [sup_class] = {}
    herf = i.find_element_by_tag_name('a')
    herf.click()
    ullist = browser.find_element_by_css_selector("[class='ullist clearfix']")
    ullist = ullist.find_elements_by_tag_name("li")
    for li in ullist:
        li = li.find_element_by_tag_name('h3')
        li = li.find_element_by_tag_name('a')
        sub_class = li.text.encode("utf-8").decode("utf-8")
        href = li.get_attribute("href").strip()
        data_per[sup_class][sub_class] = href

print(data_per)
with open(save_file, 'w') as fp:
    json.dump(data_per, fp)
sleep_sec = random.randint(start_, end_)
time.sleep(sleep_sec)
browser.quit()

