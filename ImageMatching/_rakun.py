import pymysql
import urllib.request as image_down
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

main_url = 'http://www.rakun.co.kr'
conn = pymysql.connect(host='localhost', user='djangouser', password='djangopass',
                       db='django_mysql', charset='utf8')

curs = conn.cursor()

"""necessary_list = {'outer/': ['/shop/shopbrand.html?xcode=054&type=M&mcode=003',
                             '/shop/shopbrand.html?xcode=054&type=M&mcode=002',
                             '/shop/shopbrand.html?xcode=054&type=M&mcode=001',
                             '/shop/shopbrand.html?xcode=054&type=M&mcode=004'],
                    'top/': ['/shop/shopbrand.html?xcode=055&type=M&mcode=001'],
                    'sweathers/': ['/shop/shopbrand.html?xcode=055&type=M&mcode=002'],
                    'shirts/': ['/shop/shopbrand.html?xcode=056&type=X'],
                    'slacks/': ['/shop/shopbrand.html?xcode=042&type=M&mcode=001',
                                '/shop/shopbrand.html?xcode=042&type=M&mcode=002'],
                    'jeans/': ['/shop/shopbrand.html?xcode=027&type=M&mcode=001',
                              '/shop/shopbrand.html?xcode=027&type=M&mcode=002']}"""

necessary_list = {'jacket/': ['/shop/shopbrand.html?xcode=054&type=M&mcode=003'],
                  'coat/': ['/shop/shopbrand.html?xcode=054&type=M&mcode=002'],
                  'cardigan/': ['/shop/shopbrand.html?xcode=054&type=M&mcode=001'],
                  'padding/': ['/shop/shopbrand.html?xcode=054&type=M&mcode=004']}

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
            imgs = parsing.select('td > div > ul > li > div > a > img')
            infos = parsing.select('td > div > ul > li > div > a')
            flag = 0
            index = 0
            imgs = imgs[3:]
            infos = infos[3:]

            for img in imgs:
                flag = 1
                src = img.get('src')
                if '/shopimages/rakun/' in src:
                    src = main_url + src
                    save = path + src.split('/')[-1].split('?')[0]
                    file_list = os.listdir(path)
                    file = src.split('/')[-1].split('?')[0]
                    info = infos[index]
                    href = info.get('href')
                    ref = main_url + href
                    info_url = urlopen(main_url + href)
                    info_parsing = BeautifulSoup(info_url, 'html5lib')
                    names = info_parsing.select('div > h3')
                    names = names[2].text
                    name = names.split(' ')[1:-1]
                    name = ''.join(name)
                    options = info_parsing.select('div > table > tbody > tr > td > div > span > select')
                    price = info_parsing.select('table > tbody > tr > td > div')[0].text.strip() + 'won'
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
                            curs.execute(sql, (str(name), str(photo), str(price), str(color), str(size), 'rakun', str(ref)))
                            conn.commit()

                    index += 1

            page += 1

conn.close()