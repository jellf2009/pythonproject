# -*- coding=utf8 -*-
import datetime
import random
import time
import requests
import iptest

cookiestr = 'll="118172"; bid=wYWKA4xs2Ac; __yadk_uid=zlURAzppGl6b1hU6wGIT2NGLIxNQFAgy; ' \
            '_vwo_uuid_v2=D8DABA9596735000DCCC5B729CDCF7837|57770dce540dee72040dddd441f76b93; ' \
            'ap=1; ps=y; __utmz=30149280.1528276241.5.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ' \
            '__utmz=223695111.1528276482.4.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/;' \
            ' as="https://sec.douban.com/b?r=https%3A%2F%2Fmovie.douban.com%2F";' \
            ' _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1528366117%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; ' \
            '_pk_id.100001.4cf6=4a9a61bdce226626.1528254634.6.1528366117.1528336908.; ' \
            '_pk_ses.100001.4cf6=*; __utma=30149280.497383011.1528254632.1528336908.1528366117.7; ' \
            '__utmb=30149280.0.10.1528366117; __utmc=30149280; ' \
            '__utma=223695111.1236340615.1528254634.1528336908.1528366117.6;' \
            ' __utmb=223695111.0.10.1528366117; __utmc=223695111'

hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}, {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]
headers = random.choice(hds)


def getcookiedict(cookiestr):
    list = cookiestr.split(';')
    cookiedic = {}
    for t in list:
        kv = t.strip()
        k = kv.find('=')
        key = kv[0:k]
        value = kv[k + 1:len(kv)]
        cookiedic.setdefault(key, value)
    return cookiedic


if __name__ == '__main__':
    iplist = iptest.getiplist()

    # print(iplist)
    url = "https://movie.douban.com/j/search_tags?type=movie&tag=%E7%BB%8F%E5%85%B8&source="
    # url = "http://www.ip181.com"
    # #
    html = requests.get(url, headers=headers, cookies=getcookiedict(cookiestr))
    print(html.content)
