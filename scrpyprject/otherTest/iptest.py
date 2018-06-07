# -*- coding=utf8 -*-
import requests
import random
from bs4 import BeautifulSoup
import schedule
import time
import threading
import thread

hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}, {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]
headers = random.choice(hds)


# 获取可用ip列表到文件中去
def getips():
    url = "http://www.xicidaili.com/nn/"
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.content, 'html.parser')
    iplist = soup.find('table', id='ip_list').find_all('tr')
    f = open("/root/tmp/ip.txt", 'w')

    for i in range(1, len(iplist)):
        tdlist = iplist[i].find_all('td')
        ip = tdlist[1].text
        port = tdlist[2].text
        http = tdlist[5].text.lower()
        print(http, ip, port)
        try:
            html = requests.get("https://www.baidu.com", headers=headers,
                                proxies={"{0}": "{1}://{2}:{3}".format(http, http, ip, port)}, timeout=3)
            f.write("{0}://{1}:{2}{3}".format(http, ip, port, "\n"))
        except Exception as e:
            print e
    f.close()


# 从文件中读取ipport地址
def getiplist():
    f = open("/root/tmp/ip.txt", 'r')
    ipportlist = []
    ipport = f.readlines(30)
    for ipp in ipport:
        ipportlist.append(ipp.strip())
    proxy_url_list = []

    for ip in ipportlist:
        proxy_url = {}
        if ip.find('https') == 0:
            proxy_url['https'] = ip
        else:
            proxy_url['http'] = ip
        proxy_url_list.append(proxy_url)

    return proxy_url_list


def job():
    print("定时任务执行---")
    getips()


# 做定时任务调度
def print_time():
    schedule.every(5).minutes.do(job)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    getips()
    # t = threading.Thread(target=print_time, name='worker')  # 线程对象
    # t.start()
