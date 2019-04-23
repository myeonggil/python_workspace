import pymysql
import urllib.request as image_down
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

main_url = 'http://www.a-london.co.kr'
conn = pymysql.connect(host='localhost', user='djangouser', password='djangopass',
                       db='django_mysql', charset='utf8')

curs = conn.cursor()

"""necessary_list = {'outer/': ['/shop/shopbrand.html?xcode=001&mcode=003&type=X',
                             '/shop/shopbrand.html?xcode=001&type=X&mcode=002',
                             '/shop/shopbrand.html?xcode=001&type=X&mcode=001'],
                    'top/': ['/shop/shopbrand.html?xcode=002&type=X&mcode=005'],
                    'sweathers/': ['/shop/shopbrand.html?xcode=002&type=X&mcode=002',
                                   '/shop/shopbrand.html?xcode=002&type=X&mcode=003'],
                    'shirts/': ['/shop/shopbrand.html?xcode=002&type=X&mcode=001'],
                    'slacks/': ['/shop/shopbrand.html?xcode=003&type=X&mcode=003',
                                '/shop/shopbrand.html?xcode=003&type=X&mcode=006'],
                    'jeans/': ['/shop/shopbrand.html?xcode=007&mcode=001&type=X']}"""

necessary_list = {'coat/': ['/shop/shopbrand.html?xcode=001&type=X&mcode=003'],
                    'jacket/': ['/shop/shopbrand.html?xcode=001&type=X&mcode=001'],
                    'cardigan': ['/shopbrand.html?xcode=001&type=X&mcode=002']}

sql = """insert into post_link(name, photo, price, color, size, brand, site) values(%s, %s, %s, %s, %s, %s, %s)"""
check = """select * from post_link where name=%s"""
for key, values in necessary_list.items():
    for value in values:
        path = 'Images/use_images/train/'
        path += key
        page = 1
        flag = 1
        print(value)

        while flag != 0:
            print(page)
            url_ex = urlopen(main_url + value + '&page=%d' % page)
            parsing = BeautifulSoup(url_ex, 'html5lib')
            all_tag = parsing.find_all('td', {'class': 'Brand_prodtHeight'})
            flag = 0
            index = 0

            for i in all_tag:
                flag = 1
                src = i.select('a > img')[0].get('src')
                src = main_url + src
                file_list = os.listdir(path)
                file = src.split('/')[-1].split('?')[0]
                save = path + src.split('/')[-1].split('?')[0]
                # image_down.urlretrieve(src, save)
                info = i.select('a')[0]
                href = info.get('href')
                ref = main_url + href
                info_url = urlopen(main_url + href)
                info_parsing = BeautifulSoup(info_url, 'html5lib')
                name = info_parsing.select('font > b')[0].text
                options = info_parsing.select('td > select')
                price = info_parsing.select('font > span > span')[0].text
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
                    # image_down.urlretrieve(src, save)
                    print(save)
                    curs.execute(check, (str(name)))
                    rows = curs.fetchall()
                    if len(rows) == 0:
                        curs.execute(sql, (str(name), str(photo), str(price), str(color), str(size), 'alondon', str(ref)))
                        conn.commit()

                # curs.execute(sql, (str(name), str(photo), str(price), str(color), str(size), 'a-london', str(ref)))
                # conn.commit()

                index += 1

            page += 1

conn.close()