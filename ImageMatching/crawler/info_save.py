import pymysql

conn = pymysql.connect(host='localhost', user='djangouser',
                       password='djangopass', db='django_mysql', charset='utf8')

curs = conn.cursor()

sql = "select image from matching_top_5"
curs.execute(sql)

a = curs.fetchall()
for row in a:
    print(row)