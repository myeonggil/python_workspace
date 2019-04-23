import pymysql
import urllib.request as image_down
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

main_url = 'http://www.hummingsuper.com'
conn = pymysql.connect(host='localhost', user='djangouser', password='djangopass',
                       db='django_mysql', charset='utf8')

curs = conn.cursor()

necessary_list = {'outer/': ['/product/list.html?cate_no=256',
                             '/product/list.html?cate_no=109',
                             '/product/list.html?cate_no=280',
                             '/product/list.html?cate_no=58',
                             '/product/list.html?cate_no=96',
                             '/product/list.html?cate_no=55',
                             '/product/list.html?cate_no=252'],
                    'top/': ['/product/list.html?cate_no=61'],
                    'sweathers/': ['/product/list.html?cate_no=60',
                                   '/product/list.html?cate_no=63',
                                   '/product/list.html?cate_no=89'],
                    'shirts/': ['/product/list.html?cate_no=28'],
                    'slacks/': ['/product/list.html?cate_no=77',
                                '/product/list.html?cate_no=79'],
                    'jeans/': ['/product/list.html?cate_no=51',
                               '/product/list.html?cate_no=53']}

necessary_list = {'jacket/': ['/product/list.html?cate_no=256''/product/list.html?cate_no=280', '/product/list.html?cate_no=96', '/product/list.html?cate_no=55'],
                  'padding/': ['/product/list.html?cate_no=109'],
                  'coat/': ['/product/list.html?cate_no=58'],
                    'cardigan/': ['/product/list.html?cate_no=252']}

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
            imgs = parsing.select('li > div > a > img')
            infos = parsing.select('li > div > a')
            flag = 0
            index = 0

            for img in imgs:
                flag = 1
                src = img.get('src')
                if '/web/product/medium/' in src:
                    src = 'http:' + src
                    save = path + src.split('/')[-1]
                    file_list = os.listdir(path)
                    file = src.split('/')[-1]
                    info = infos[index]
                    href = info.get('href')
                    ref = main_url + href
                    info_url = urlopen(main_url + href)
                    info_parsing = BeautifulSoup(info_url, 'html5lib')
                    name = info_parsing.select('div > h3')[0].text
                    options = info_parsing.select('td > select')[:2]
                    price = info_parsing.select('tr > td')[2].text
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
                            curs.execute(sql,(str(name), str(photo), str(price), str(color), str(size), 'hummingsuper', str(ref)))
                            conn.commit()

                    index += 1

            page += 1

conn.close()