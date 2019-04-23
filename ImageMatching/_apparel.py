import pymysql
import urllib.request as image_down
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

main_url = 'http://www.koreanapparel.co.kr'
conn = pymysql.connect(host='localhost', user='djangouser', password='djangopass',
                       db='django_mysql', charset='utf8')

curs = conn.cursor()

necessary_list = {'outer/': ['/shop/shopbrand.html?type=X&xcode=008&mcode=005&sort=', '/shop/shopbrand.html?type=X&xcode=008&mcode=013&sort=',
                   '/shop/shopbrand.html?type=X&xcode=008&mcode=003&sort=', '/shop/shopbrand.html?type=X&xcode=008&mcode=001&sort=',
                   '/shop/shopbrand.html?type=X&xcode=008&mcode=008&sort=', '/shop/shopbrand.html?type=X&xcode=008&mcode=006&sort=',
                   '/shop/shopbrand.html?type=X&xcode=008&mcode=007&sort=', '/shop/shopbrand.html?type=X&xcode=008&mcode=004&sort=',
                   '/shop/shopbrand.html?type=X&xcode=008&mcode=011&sort=', '/shop/shopbrand.html?type=X&xcode=008&mcode=012&sort='],
                    'top/': ['/shop/shopbrand.html?type=X&xcode=010&mcode=002&sort='],
                    'sweathers/': ['/shop/shopbrand.html?xcode=010&type=M&mcode=001',
                                   '/shop/shopbrand.html?type=X&xcode=010&mcode=001&sort=',
                                   '/shop/shopbrand.html?type=X&xcode=010&mcode=004&sort=',
                                   '/shop/shopbrand.html?type=X&xcode=010&mcode=007&sort='],
                    'shirts/': ['/product/list.html?cate_no=546'],
                    'slacks/': ['/shop/shopbrand.html?type=X&xcode=011&mcode=001&sort=',
                                '/shop/shopbrand.html?type=X&xcode=011&mcode=003&sort=',
                                '/shop/shopbrand.html?type=X&xcode=011&mcode=009&sort='],
                    'jeans/': ['/shop/shopbrand.html?type=X&xcode=011&mcode=002&sort=']}

sql = """insert into post_link(name, photo, price, color, size, brand, site) values(%s, %s, %s, %s, %s, %s, %s)"""
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
            imgs = parsing.select('div > div > ul > li > ul > li > div > a > img')[4:]
            infos = parsing.select('div > div > ul > li > ul > li > div > a')[4:]
            flag = 0
            index = 0
            start = 0

            for img in imgs:
                flag = 1
                src = img.get('src')
                src = main_url + src
                file_list = os.listdir(path)
                file = src.split('/')[-1]
                save = path + src.split('/')[-1]
                # image_down.urlretrieve(src, save)
                info = infos[index]
                href = info.get('href')
                ref = main_url + href
                info_url = urlopen(main_url + href)
                info_parsing = BeautifulSoup(info_url, 'html5lib')
                name = info_parsing.find('td', {'class': 'tit-prd'}).get_text()
                options = info_parsing.select('dd > select')
                price = info_parsing.find('td', {'class': 'price'}).get_text().strip()
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
                    print(src)
                    curs.execute(sql, (str(name), str(photo), str(price), str(color), str(size), 'apparel', str(ref)))
                    conn.commit()

                # curs.execute(sql, (str(name), str(photo), str(price), str(color), str(size), 'koreanapparel', str(ref)))
                # conn.commit()

                index += 1

            page += 1

conn.close()