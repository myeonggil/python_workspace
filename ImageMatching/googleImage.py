from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ast
import urllib.request as image_down
import os
from learning.load_tensor import learning
import ex


driver = webdriver.Chrome('C:\Anaconda3\envs\TensorFlow\Scripts\chromedriver')
driver.get('https://www.google.co.kr/imghp?hl=ko')

try:
    # WebDriverWait와 .until 옵션을 통해 우리가 찾고자 하는 HTML 요소를
    # 기다려 줄 수 있습니다.
    driver.find_element_by_class_name('gsst_a').click()
    driver.find_element_by_xpath('//*[@id="qbug"]/div/a').click()
    driver.find_element_by_xpath('//*[@id="qbfile"]').send_keys(os.getcwd() + '/ccnp.png')
    title = WebDriverWait(driver, 10) \
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h3 > a')))
    url = title.get_attribute('href')

    text = requests.get(url, headers={
        'user-agent': ':Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}).text

    bs = BeautifulSoup(text, 'html.parser')
    for i in bs.find_all('div', {'class': 'rg_meta'}):
        dictionary = ast.literal_eval(i.text)
        print(dictionary)
        # print(dictionary['ru'], dictionary['ou'])
        """path = 'zipp/'
        name = str(dictionary['ou']).split('/')[-1]
        if name[-1] == 'g':
            path += name
            try:
                image_down.urlretrieve(dictionary['ou'], path)
            except:
                print('error')

    image_list = os.listdir('./zipp')
    for i in image_list:
        path = '../zipp/'
        path += i
        print(learning(path))"""
finally:
    driver.quit()
