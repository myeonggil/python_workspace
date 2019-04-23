import pymysql
import urllib.request as image_down
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

main_url = 'http://tovintage.co.kr'
conn = pymysql.connect(host='localhost', user='djangouser', password='djangopass',
                       db='django_mysql', charset='utf8')

curs = conn.cursor()

"""necessary_list = {'outer/': ['/product/list.html?cate_no=48',
                             '/product/list.html?cate_no=60',
                             '/product/list.html?cate_no=61',
                             '/product/list.html?cate_no=62',
                             '/product/list.html?cate_no=63',
                             '/product/list.html?cate_no=64'],
                    'top/': ['/product/list.html?cate_no=68'],
                    'sweathers/': ['/product/list.html?cate_no=65',
                                   '/product/list.html?cate_no=66',
                                   '/product/list.html?cate_no=67',
                                   '/product/list.html?cate_no=71'],
                    'shirts/': ['/product/list.html?cate_no=29'],
                    'slacks/': ['/product/list.html?cate_no=77'],
                    'jeans/': ['/product/list.html?cate_no=78']}"""

necessary_list = {'coat/': ['/product/list.html?cate_no=48'],
                  'jacket/': ['/product/list.html?cate_no=60', '/product/list.html?cate_no=61', '/product/list.html?cate_no=64'],
                  'cardigan/': ['/product/list.html?cate_no=62'],
                  'padding/': ['/product/list.html?cate_no=63']}

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
            imgs = parsing.select('div > ul > li > a > img')
            infos = parsing.find_all('a', {'class': 'prdImg'})
            flag = 0
            index = 0
            start = 0

            for i in infos:
                href = i.get('href')
                if 'group=2' in href:
                    start += 1

            imgs = imgs[start + 2:]
            infos = infos[start:]

            for img in imgs:
                flag = 1
                src = img.get('src')
                if '/web/product/big/' in src:
                    src = 'http:' + src
                    save = path + src.split('/')[-1]
                    file_list = os.listdir(path)
                    file = src.split('/')[-1]
                    info = infos[index]
                    href = info.get('href')
                    ref = main_url + href
                    info_url = urlopen(main_url + href)
                    info_parsing = BeautifulSoup(info_url, 'html5lib')
                    name = img.get('alt')
                    options = info_parsing.select('td > select')[:2]
                    price = info_parsing.select('span > strong')[0].text + 'won'
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

                    # print(name, photo, price, color, size, ref)

                    if file not in file_list:
                        temp = []
                        image_down.urlretrieve(src, save)
                        print(save)
                        curs.execute(check, (str(name)))
                        rows = curs.fetchall()
                        if len(rows) == 0:
                            print('신규')
                            curs.execute(sql, (str(name), str(photo), str(price), str(color), str(size), 'vintage', str(ref)))
                            conn.commit()

                    index += 1

            page += 1

conn.close()