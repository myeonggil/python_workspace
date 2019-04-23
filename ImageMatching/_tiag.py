import pymysql
import urllib.request as image_down
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

main_url = 'http://www.tiag.co.kr'
conn = pymysql.connect(host='localhost', user='djangouser', password='djangopass',
                       db='django_mysql', charset='utf8')

curs = conn.cursor()

"""necessary_list = {'outer/': '/product/list.html?cate_no=27',
                    'top/': '/product/list.html?cate_no=107',
                    'slacks/': '/product/list.html?cate_no=99',
                    'jeans/': '/product/list.html?cate_no=102',
                    'shirts/': '/product/list.html?cate_no=29',
                  'sweathers/': '/product/list.html?cate_no=105'}"""

necessary_list = {
                  'jacket/': '/product/list.html?cate_no=96'}

sql = """insert into post_link(name, photo, price, color, size, brand, site) values(%s, %s, %s, %s, %s, %s, %s)"""
check = """select * from post_link where name=%s"""
for key, value in necessary_list.items():
    path = 'Images/use_images/train/'
    path += key
    page = 1
    flag = 1
    print(value)

    while flag != 0:
        print(page)
        url_ex = urlopen(main_url + value + '&page=%d' % page)
        parsing = BeautifulSoup(url_ex, 'html5lib')
        imgs = parsing.select('li > div > a > img')
        infos = parsing.select('li > div > a')
        flag = 0
        index = 0

        if value.split('=')[-1] == '29' or value.split('=')[-1] == '27':
            imgs = imgs[4:]
            infos = infos[4:]

        for img in imgs:
            flag = 1
            src = img.get('src')
            src = 'http:' + src
            file_list = os.listdir(path)
            file = src.split('/')[-1]
            save = path + src.split('/')[-1]
            # image_down.urlretrieve(src, save)
            info = infos[index]
            href = info.get('href')
            ref = main_url + href
            info_url = urlopen(main_url + href)
            info_parsing = BeautifulSoup(info_url, 'html5lib')
            names = info_parsing.select('div > div > div > div > meta')
            options = info_parsing.select('table > tbody > tr > td > select')
            name = str(names[0].get('content')).split('<br>')[-1]
            price = names[2].get('content') + 'won'
            photo = '../../' + save

            if len(options) == 1:
                color = options[0].text
                size = ''
            elif len(options) == 2:
                color = options[0].text
                size = options[1].text
            else:
                color = ''
                size = ''

            if file not in file_list:
                temp = []
                image_down.urlretrieve(src, save)
                print(save)
                curs.execute(check, (str(name)))
                rows = curs.fetchall()
                if len(rows) == 0:
                    print('신규')
                    curs.execute(sql, (str(name), str(photo), str(price), str(color), str(size), 'tiag', str(ref)))
                    conn.commit()
            # curs.execute(sql, (str(name), str(photo), str(price), str(color), str(size), 'TIAG', str(ref)))
            # conn.commit()

            index += 1

        page += 1

conn.close()