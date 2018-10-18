#coding:utf-8
from selenium import webdriver
import os
from selenium.webdriver.common.action_chains import ActionChains #引入ActionChains鼠标操作类
from selenium.webdriver.common.keys import Keys #引入keys类操作
import time
import random
import json


chrome_driver_path = './chromedriver'
home_page = 'http://baidu.com'
save_file = 'sub_class_file.txt'
data = {}
start_ = 3
end_ = 16
continue_text = '>'

browser = webdriver.Chrome(chrome_driver_path)
browser.get(home_page)
with open('sub_class_file.txt', 'r') as file_d:
    data = json.loads(file_d.read())

for sup in data.keys():
    handle_list = []
    current_handle = browser.current_window_handle
    handle_list.append(current_handle)
    path = os.path.join('data', sup)
    if not os.path.exists(path):
        os.mkdir(path)
    for sub in data[sup].keys():
        sub_path = os.path.join(path, sub)
        if not os.path.exists(sub_path):
            os.mkdir(sub_path)
        htm = data[sup][sub]
        htm_js = 'window.open(\"' + htm + '\");'
        browser.execute_script(htm_js)
        next_handle = None
        for i in browser.window_handles:
            if i not in handle_list:
                next_handle = i
                handle_list.append(next_handle)
        browser.switch_to.window(next_handle)

        while True:
            next_page_is_click = False
            if next_page_is_click == True:
                handle_list.remove(next_handle)
                new_handle = browser.current_window_handle
                next_handle = new_handle
                handle_list.append(next_handle)
                next_page_is_click = False
                browser.switch_to.window(next_handle)
                time.sleep(random.randint(10,30))
            page = browser.find_element_by_id('page')
            container = page.find_element_by_id('container')
            time.sleep(2)
            next_page_exist = 1
            try:
                cor = container.find_elements_by_class_name('n')
                next_page = cor[0]
                next_page = next_page.find_element_by_tag_name('a')
                next_page_exist = 1 if next_page.text.strip() == continue_text else 0
            except:
                next_page_exist = 0
                print('exception')
            common_bd = container.find_element_by_css_selector("[class='common_bd clearfix']")
            common_main = common_bd.find_element_by_class_name('common_main')
            result_folder = common_main.find_element_by_css_selector("[class='m49 result']")
            result_folder = result_folder.find_elements_by_tag_name('li')
            pre_handle = browser.current_window_handle
            for li in result_folder:
                time.sleep(random.randint(5,15))
                try:
                    a_tag = li.find_element_by_tag_name('a')
                    href = a_tag.get_attribute("href")
                    href_js = 'window.open(\"' + href + '\");'
                    browser.execute_script(href_js)
                except:
                    continue
                next_handle = None
                for h in browser.window_handles:
                    if h not in handle_list:
                        next_handle = h
                        handle_list.append(next_handle)
                browser.switch_to.window(next_handle)
                try:
                    frame = browser.find_element_by_css_selector("[class='m49 detail detail1']")
                except:
                    print('move')
                    handle_list.remove(next_handle)
                    browser.close()
                    browser.switch_to.window(pre_handle)
                    continue
                dl = frame.find_element_by_tag_name('dl')
                dt_list = dl.find_elements_by_tag_name('dt')
                dd_list = dl.find_elements_by_tag_name('dd')
                med_info = {}
                med_name = ''
                med_prod = ''
                '''
                for dt, dd in zip(dt_list, dd_list):
                    dt_text = dt.text.strip()[:-1]
                    dd_text = ''
                    exist_flag = True
                    ele_list = None
                    try:
                       ele_list = dd.find_elements_by_css_selector('*')
                    except:
                        exist_flag = False
                        print('false')
                    if exist_flag is True:
                        for e in ele_list:
                            dd_text += e.text.strip() + ';'
                        dd_text = dd_text[:-1]
                    else:
                        dd_text = dd.text.strip()
                    if dt_text == '药品名称':
                        med_name = dd_text
                    elif dt_text == '生产企业':
                        med_prod = dd_text
                    med_info[dt_text] = dd_text
                '''
                for dt, dd in zip(dt_list, dd_list):
                    dt_text = dd.text.strip()[:-1]
                    dd_text = ''
                    print(dd.get_attribute('innerHTML'))
                print(med_prod + ' '+med_name)
                file_path = os.path.join(sub_path, med_name+'-'+med_prod+'.txt')
                with open(file_path, 'w') as file_d:
                   json.dump(med_info, file_d)
                handle_list.remove(next_handle)
                browser.close()
                try:
                    browser.switch_to.window(pre_handle)
                except:
                    handle_list_
            if next_page_exist is 0:
                break
            else:
                next_page_is_click = True
                try:
                    next_page.click()
                except:
                    handle_list.remove()

        browser.close()

    def is_sub_element_exist(driver):
        try:
            driver.find_element_by_css(".")
            return True
        except:
            return False

    def process_sub_element(driver):
        rs = ''
        s = driver.find_elemenet_by_css('*')
        for i in s:
            rs += i.text + ';'
        return rs
