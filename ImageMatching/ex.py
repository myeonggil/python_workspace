import pymysql
import os
import learning.imagenet_example as classification


# classification.run_inference_on_image('learning/1e9b20b84b8f197e22fc7dc8578feb31.jpg')
"""conn = pymysql.connect(host='localhost', user='djangouser', password='djangopass',
                       db='django_mysql', charset='utf8')

curs = conn.cursor()

cardigan = os.listdir('Images/use_images/train/cardigan')
coat = os.listdir('Images/use_images/train/coat')
jacket = os.listdir('Images/use_images/train/jacket')
padding = os.listdir('Images/use_images/train/padding')

sql1 = update post_link set photo=%s where photo like %s
sql2 = select photo from post_link where photo like %s

dictionary = {}
dictionary['cardigan'] = cardigan
dictionary['coat'] = coat
dictionary['jacket'] = jacket
dictionary['padding'] = padding

for key, values in dictionary.items():
    for value in values:
        curs.execute(sql2, ('%' + str(value)))
        rows = curs.fetchone()
        if rows != None:
            row = str(rows[0]).replace('outer', key)
            curs.execute(sql1, (row, '%' + row.split('/')[-1]))
            conn.commit()
    print(key + " 완료")"""

"""curs.execute(check, (str(name)))
rows = curs.fetchall()
if len(rows) == 0:
    print('신규')
    curs.execute(sql, (str(name), str(photo), str(price), str(color), str(size), 'vintage', str(ref)))
    conn.commit()"""

"""if flag == 1:
    driver = webdriver.Chrome('C:\Anaconda3\envs\TensorFlow\Scripts\chromedriver')
    driver.get('https://www.google.co.kr/imghp?hl=ko')
    try:
        driver.find_element_by_class_name('gsst_a').click()
        driver.find_element_by_xpath('//*[@id="qbug"]/div/a').click()
        driver.find_element_by_xpath('//*[@id="qbfile"]').send_keys(google_input_image)
        # WebDriverWait와 .until 옵션을 통해 우리가 찾고자 하는 HTML 요소를
        # 기다려 줄 수 있습니다.
        title = WebDriverWait(driver, 10) \
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3 > a")))
        url = title.get_attribute('href')

        text = requests.get(url, headers={
            'user-agent': ':Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}).text

        bs = BeautifulSoup(text, 'html.parser')
        page_src = {}

        index = 1
        for i in bs.find_all('div', {'class': 'rg_meta'}):
            dictionary = ast.literal_eval(i.text)
            # print(dictionary['ru'], dictionary['ou'])
            path = google_img_path + '/'
            name = str(dictionary['ou']).split('/')[-1]
            path += '%s.jpg' % index
            try:
                image_down.urlretrieve(dictionary['ou'], path)
                page_src['%s.jpg' % str(index)] = dictionary['ru']
                index += 1
            except:
                print('error')

        path = google_img_path
        image_list = os.listdir(path)
        temp = {}
        for i in image_list:
            path = google_img_path + '/'
            path += i
            google_key, google_value = google_learning(path)
            if google_key == locate:
                a = math.fabs(value - google_value)
                temp[a] = path

        sorted(temp.items(), key=operator.itemgetter(1))
        index = 0
        sql = insert into post_google_result(author_id, user_id, google_img, google_src) values(%s, %s, %s, %s)
        for key, value in temp.items():
            if index < 10:
                check = str(value).split('/')[-1]
                curs.execute(sql, (str(post.author_id), str(post.id), str(page_src[check]), '../.' + str(value)))
                conn.commit()

            index += 1

    finally:
        driver.quit()"""

a = {}
a["a"] = 1
a["b"] = 2
print(a)