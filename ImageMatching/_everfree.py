import pymysql
import urllib.request as image_down
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

main_url = 'http://www.everfree.co.kr'
conn = pymysql.connect(host='localhost', user='djangouser', password='djangopass',
                       db='django_mysql', charset='utf8')

curs = conn.cursor()

"""necessary_list = {'outer/': ['/shop/shopbrand.html?type=X&xcode=015&mcode=004',
                             '/shop/shopbrand.html?type=X&xcode=015&mcode=001',
                             '/shop/shopbrand.html?type=X&xcode=015&mcode=002',
                             '/shop/shopbrand.html?type=X&xcode=015&mcode=003'],
                    'top/': ['/shop/shopbrand.html?type=X&xcode=013&mcode=007'],
                    'sweathers/': ['/shop/shopbrand.html?type=X&xcode=007'],
                    'shirts/': ['/shop/shopbrand.html?type=X&xcode=012'],
                    'slacks/': ['/shop/shopbrand.html?type=X&xcode=014&mcode=003',
                                '/shop/shopbrand.html?type=X&xcode=014&mcode=004'],
                    'jeans/': ['/shop/shopbrand.html?type=X&xcode=002']}"""

necessary_list = {'cardigan/': ['/shop/shopbrand.html?type=X&xcode=015&mcode=004'],
                  'jacket/': ['/shop/shopbrand.html?type=X&xcode=015&mcode=001'],
                  'coat/': ['/shop/shopbrand.html?type=X&xcode=015&mcode=002'],
                  'padding/': ['/shop/shopbrand.html?type=X&xcode=015&mcode=003']}

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
            url_ex = urlopen(main_url + value + '&sort=&page=%d' % page)
            parsing = BeautifulSoup(url_ex, 'html5lib')
            im = parsing.select('div > div > div > div > a > div > ul > li')
            for i in im:
                print(i.find_all('div', {'class': 'primary'}))
                print('\n')
            imgs = parsing.select('div > a > ul > li > img')[4:]
            """infos_all = parsing.select('div > div > div > div > div > a')
            infos = []
            flag = 0
            index = 0
            print(imgs)

            for i in infos_all:
                a = i.get('href')
                if '/shop/shopdetail.html?branduid=' in a:
                    infos.append(a)

            infos = infos[4:]

            for img in imgs:
                flag = 1
                src = img.get('src')
                src = main_url + src
                file_list = os.listdir(path)
                file = src.split('/')[-1].split('?')[0]
                save = path + src.split('/')[-1].split('?')[0]
                # image_down.urlretrieve(src, save)
                info = infos[index]
                # href = info.get('href')
                ref = main_url + info
                info_url = urlopen(main_url + info)
                info_parsing = BeautifulSoup(info_url, 'html5lib')
                name = info_parsing.select('div > div > div > ul > li')[17].text.strip()
                options = info_parsing.select('div > div > div > ul > li')[20:22]
                price = info_parsing.select('div > div > div > ul > li')[18].text.strip()
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

                size = info_parsing.select('div > div > div > ul > li')[20].text
                color = info_parsing.select('div > div > div > ul > li')[22].text

                if file not in file_list:
                    temp = []
                    image_down.urlretrieve(src, save)
                    print(save)
                    curs.execute(check, (str(name)))
                    rows = curs.fetchall()
                    if len(rows) == 0:
                        print('신규')
                        curs.execute(sql, (str(name), str(photo), str(price), str(color), str(size), 'everfree', str(ref)))
                        conn.commit()

                # print(name, photo, price, color, size, ref)

                # curs.execute(sql, (str(name), str(photo), str(price), str(color), str(size), 'everfree', str(ref)))
                # conn.commit()

                index += 1"""

            page += 1

conn.close()