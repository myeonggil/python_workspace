import pymysql
import urllib.request as image_down
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

main_url = 'http://dj2.co.kr'
conn = pymysql.connect(host='localhost', user='djangouser', password='djangopass',
                       db='django_mysql', charset='utf8')

curs = conn.cursor()

"""necessary_list = {'outer/': ['/product/list.html?cate_no=533',
                             '/product/list.html?cate_no=1352',
                             '/product/list.html?cate_no=537',
                             '/product/list.html?cate_no=531',
                             '/product/list.html?cate_no=557'],
                    'top/': ['/product/list.html?cate_no=542'],
                    'sweathers/': ['/product/list.html?cate_no=541',
                                   '/product/list.html?cate_no=1275',
                                   '/product/list.html?cate_no=1009'],
                    'shirts/': ['/product/list.html?cate_no=546'],
                    'slacks/': ['/product/list.html?cate_no=1353',
                                '/product/list.html?cate_no=554'],
                    'jeans/': ['/product/list.html?cate_no=552',
                              '/product/list.html?cate_no=1354']}"""

necessary_list = {'jacket/': ['/product/list.html?cate_no=533'],
                  'coat/': ['/product/list.html?cate_no=1352'],
                  'cardigan/': ['/product/list.html?cate_no=537'],
                  'padding/': ['/product/list.html?cate_no=531']}

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
            a = parsing.find_all('div', {'class': 'box'})[:-1]
            imgs = []
            infos = []

            for i in a:
                imgs.append(i.select('a > img'))
                infos.append(i.select('a'))

            flag = 0
            index = 0
            start = 0

            for i in infos:
                href = i[0].get('href')
                if 'group=2' in href:
                    start += 1

            imgs = imgs[start:]
            infos = infos[start:]

            for img in imgs:
                flag = 1
                src = img[0].get('src')
                src = 'http:' + src
                file_list = os.listdir(path)
                file = src.split('/')[-1]
                save = path + src.split('/')[-1]
                # image_down.urlretrieve(src, save)
                info = infos[index]
                href = info[0].get('href')
                ref = main_url + href
                info_url = urlopen(main_url + href)
                info_parsing = BeautifulSoup(info_url, 'html5lib')
                name = info_parsing.select('div > h3')[-5].text
                options = info_parsing.select('tbody > tr > td > select')
                price = info_parsing.select('td > span > strong')[0].text
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
                        curs.execute(sql, (str(name), str(photo), str(price), str(color), str(size), 'dj2', str(ref)))
                        conn.commit()

                # curs.execute(sql, (str(name), str(photo), str(price), str(color), str(size), 'dj2', str(ref)))
                # conn.commit()

                index += 1

            page += 1

conn.close()