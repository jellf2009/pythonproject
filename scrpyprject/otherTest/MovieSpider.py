# -*- coding=utf8 -*-
import requests
import json
import MySQLdb
import datetime
from bs4 import BeautifulSoup
import random
import time
import iptest

con = MySQLdb.connect('127.0.0.1', 'root', 'root', 'firstTest', charset='utf8')
cursor = con.cursor()
hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}, {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]
headers = random.choice(hds)

iplist = iptest.getiplist()


def insertIntoMysql(tag, name, score, content, imageurl, directer, actors, uptime):
    try:
        sql = "insert into movie(tag,movie_name,score,content,image_url,create_time,directer,actors,uptime" \
              ") VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"

        datestr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = sql % (tag, name, score, content, imageurl, datestr, directer, actors, uptime)
        cursor.execute(sql)
        print(u"添加成功--> %s" % sql)
        con.commit()
    except Exception as e:
        print(e)
        print(sql)
        print("数据插入失败")


def findAllTags():
    url = "https://movie.douban.com/j/search_tags?type=movie&tag=%E7%BB%8F%E5%85%B8&source="
    html = requests.get(url, headers=headers, proxies={"http": random.choice(iplist)})
    result = json.loads(html.content)
    print(result)
    return result.get('tags')


def saveimage(imageurl, title):
    img = requests.get(imageurl, headers=headers, proxies={"http": random.choice(iplist)})
    f = open("/root/tmp/img/%s.jpg" % title, 'wb')
    f.write(img.content)
    f.close()


def saveAll(subjects, tag):
    errorurl = ''
    try:
        for subject in subjects:
            title = subject['title']
            imageurl = subject['cover']
            score = subject['rate']
            url = subject['url']
            errorurl = url
            html = requests.get(url, headers=headers, proxies={"http": random.choice(iplist)})
            soup = BeautifulSoup(html.text, "html.parser")

            contentinfo = soup.find('div', id="link-report").find('span', property="v:summary")
            content = contentinfo.text.strip()
            content = content.replace('\n', '').replace("  ", "")

            allinfo = soup.find('div', id="info")
            directer = allinfo.find('a', rel="v:directedBy")
            uptime = allinfo.find('span', property="v:initialReleaseDate")
            actors = allinfo.find_all('a', rel="v:starring")

            initActors = []
            countActor = 0
            for actor in actors:
                countActor = countActor + 1
                if countActor <= 5:
                    initActors.append(actor.text)
            Allactors = ",".join(initActors)

            insertIntoMysql(tag, title, score, content, imageurl, directer.text, Allactors, uptime.text)
            saveimage(imageurl, title)
    except Exception as e:
        print(e)
        f = open("/root/tmp/img/errorurl.txt", 'wb')
        f.write(errorurl + "\n")
        f.close()
        print('出现错误没有找到属性')


def spaiderData():
    tags = findAllTags()
    for tag in tags:
        for x in range(0, 1000, 20):
            url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%s&sort=recommend&page_limit=20&page_start=%s" % \
                  (tag, x)

            html = requests.get(url, headers=headers, proxies={"http": random.choice(iplist)})
            result = json.loads(html.content)
            subjects = result.get('subjects')
            if len(subjects) != 0:
                saveAll(subjects, tag)
            else:
                break


if __name__ == '__main__':
    print datetime.datetime.now()
    spaiderData()
    ran = random.random() * 2
    time.sleep(ran)
    print datetime.datetime.now()
