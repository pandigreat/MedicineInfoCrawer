from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains #引入ActionChains鼠标操作类
from selenium.webdriver.common.keys import Keys #引入keys类操作
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import json
import os
import traceback
import re

class Spider():
    def __init__ (self, dict_file, ip_file, chrome_dirver, save_file_dir, wait_time=30, home_page='http://drug.dxy.cn'):
        self.dict = json.load(open(dict_file, 'r'))
        self.ip_list = []
        with open(ip_file, 'r') as file_d:
            for ip in file_d:
                self.ip_list.append(ip.strip())
        self.chrome_driver = chrome_dirver
        self.browser = webdriver.Chrome(chrome_dirver)
        self.home_page = home_page
        self.save_file_dir = save_file_dir
        self.wait_time = wait_time
        self.log = {}
        self.ERROR_INFO = 'ERR_SPDY_PROTOCOL_ERROR'
        self.log_name = os.path.join('log','log_'+ time.asctime() + '.txt')
        for key in self.dict.keys():
            self.log[key] = {}
            for k in self.dict[key]:
                self.log[key][k] = False

    def log(self, **param):
        with open(self.log_name, 'a+')as fp:
            fp.write('')

    def start(self):
        self.browser.get(self.home_page)

    def save_file(self, save_file_dir,  sup_dir, sub_file, file_name, content):
        path = os.path.join(save_file_dir, sup_dir)
        if not os.path.exists(path):
            os.mkdir(path)
        path = os.path.join(path, sub_file)
        if not os.path.exists(path):
            os.mkdir(path)
        file_d = os.path.join(path, file_name)
        with open(file_d, 'w') as file_p:
            json.dump(content, file_p)

    def test_proxy(self, proxy):
        pass


    def find_proxy(self, ip):
        random.shuffle(self.ip_list)
        proxy_ip = self.ip_list[0]
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': proxy_ip
        })
        opt = webdriver.ChromeOptions()
        opt.add_argument('--proxy-server=http://'+proxy_ip)
        self.browser = webdriver.Chrome(self.chrome_driver, chrome_options=opt)
        flag = True
        locator = (By.LINK_TEXT, '丁香园')
        try:
            self.browser.get(ip)
            self.browser.find_element_by_id('head')
            WebDriverWait(self.browser, 10, 0.5).until(EC.presence_of_element_located(locator))

        except:
            flag = False
            self.browser.quit()
        finally:
            ip = proxy_ip
            return flag
        '''
        self.browser = webdriver.Chrome(self.chrome_driver, proxy=proxy)
        self.browser.get(self.home_page)
        source_page = self.browser.page_source
        if self.ERROR_INFO in source_page:
            self.browser.quit()
            return False
        self.browser.quit()
        return True
        '''

    def set_proxy(self, ip):
        ip = ip
        while self.find_proxy(ip) is True:
            break
        pass
        #opt = webdriver.ChromeOptions()
        #opt.add_argument('--proxy-server=http://' + ip)
        #self.browser = webdriver.Chrome(self.chrome_driver, chrome_options=opt)

    def login(self):
        passwd = 'pandi65376122'
        user = 'pandigreat@163.com'
        self.browser.get(self.home_page)
        nav = self.browser.find_element_by_id('nav')
        herf = nav.find_elements_by_tag_name('a')[0]
        herf.click()
        current_handle = self.browser.current_window_handle
        self.browser.switch_to.window(current_handle)
        nav = self.browser.find_element_by_class_name('login__tab_wp')
        href = nav.find_elements_by_tag_name("a")
        href = href[1]
        href.click()
        panel = self.browser.find_element_by_class_name('J-account-login')
        inputs = panel.find_elements_by_class_name('login__input')
        u = ActionChains(self.browser).move_to_element(inputs[0])
        p = ActionChains(self.browser).move_to_element(inputs[1])
        inputs[0].send_keys(user)
        inputs[1].send_keys(passwd)
        button = self.browser.find_element_by_class_name('button')
        button.click()
        time.sleep(20)



    def process_panel_data(self, key, v):
        val = v.get_attribute('innerHTML')
        #vals = v.get_attribute('innerTEXT')
        #print(vals)
        rs_key = key.text.strip()[:-1]
        #print(rs_key)
        rs_val = ''
        pattern = re.compile('<[^>]*>')
        rs_val = pattern.sub(';',val)
        rs_val = rs_val.replace(' ', '')
        rs_val = rs_val.replace('\t', '')
        rs_val = rs_val.replace('\n', '')
        rs_val = rs_val.replace('\r', '')
        #print(rs_val)
        with open('txt.txt', 'a+') as fp:
            fp.write(rs_val)
        return (rs_key, rs_val)


    def run(self):
        count = 0
        for sup in self.dict.keys():
            for sub in self.dict[sup].keys():
                #Get Available Proxy ip address
                # Get Pages of result list
                self.login()
                html = self.dict[sup][sub]
                #self.set_proxy(html)
                total_page = -1
                flag = True
                while flag:
                    try:
                        if count % 1 == 0:
                            browser = self.browser
                            browser.get(html)
                        else:
                            random.shuffle(self.ip_list)
                            ip = self.ip_list[0].strip()
                            opt = webdriver.ChromeOptions()
                            opt.add_argument('--proxy-server=http://' + ip)
                            self.browser = webdriver.Chrome(self.chrome_driver, chrome_options=opt)
                        flag = False
                    except:
                        browser.quit()
                        time.sleep(random.randint(20))

                #browser = self.browser
                #browser.get(html)
                container = browser.find_element_by_id('container')
                cor = container.find_element_by_css_selector("[class='fr f12 result-status']")
                cor = cor.find_element_by_tag_name('span').text
                cor = int(cor)
                total_page = int(cor / 10 + 1)
                #spide one page of result
                for page_num in range(1, total_page+1):
                    url = self.dict[sup][sub] + "?page=" + str(page_num)
                    try:
                        browser.get(url)
                    except:
                        traceback.print_exc()
                        continue
                    container = browser.find_element_by_id('container')
                    common_bd = container.find_element_by_css_selector("[class='common_bd clearfix']")
                    common_main = common_bd.find_element_by_class_name('common_main')
                    result_folder = common_main.find_element_by_css_selector("[class='m49 result']")
                    result_folder = result_folder.find_elements_by_tag_name('li')
                    pre_handle = browser.current_window_handle

                    for id ,li in enumerate(result_folder):
                        if id == 10:
                            break;
                        #switch next level page
                        page_handle = None
                        time.sleep(random.randint(9,12))
                        try:
                            a_tag = li.find_element_by_tag_name('a')
                            href = a_tag.get_attribute("href")
                            href_js = 'window.open(\"' + href + '\");'
                            browser.execute_script(href_js)
                            handle_list = browser.window_handles
                            page_handle = handle_list[0] if handle_list[1] == pre_handle else handle_list[1]
                            browser.switch_to.window(page_handle)
                        except:
                            traceback.print_exc()
                            continue

                        #Start spidering
                        frame = None
                        try:
                            frame = browser.find_element_by_css_selector("[class='m49 detail detail1']")
                            frame = frame.find_element_by_tag_name('dl')
                        except:
                            traceback.print_exc()
                            continue

                        dt_list = frame.find_elements_by_tag_name('dt')
                        dd_list = frame.find_elements_by_tag_name('dd')
                        med_info = {}
                        (med_name, med_prod )= '', ''
                        for dt, dd in zip(dt_list, dd_list):
                            key, val = self.process_panel_data(dt, dd)
                            med_info[key] = val
                        med_name = med_info['药品名称']

                        med_prod = med_info['生产企业']

                        #Dump the message into a file with json format
                        med_name = med_name.split(';')[0].split("：")[1]
                        file_name = med_name + '-' + med_prod + '.txt'
                        print(med_prod)
                        self.save_file(self.save_file_dir, sup, sub, file_name, med_info)
                        #Switch to pre page
                        #time.sleep(random.randint(10, 20))
                        browser.close()
                        browser.switch_to.window(pre_handle)
                    browser.quit()
                    #time.sleep(random.randint(30, 60))


if __name__ == '__main__':
    print('start')
    dict_file = './sub_class_file.txt'
    ip_file = './ips.txt'
    chrome_driver = './chromedriver.exe'
    save_file = 'data'
    spider = Spider(dict_file, ip_file, chrome_driver, save_file)
    spider.start()
    spider.run()
