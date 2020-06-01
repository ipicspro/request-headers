# -*- coding: utf-8 -*-

import json
import csv
import random
import requests
from requests.exceptions import ConnectionError, ReadTimeout, Timeout
from fake_useragent import UserAgent, settings as fake_setttings
from fake_useragent import FakeUserAgentError
from bs4 import BeautifulSoup as bs
import time

import multiprocessing as mp




def get_file_rows(obj, encoding='utf-8'):
    '''
    read lines from file to list
    '''
    cfile = None
    try:
        lf = []
        with open(obj, 'r', encoding=encoding) as f:  # 'utf-8-sig'
            csv_f = csv.reader(f)
            lf = list(csv_f)
        cfile = []
        for a in lf:
            cfile.append(tuple(a))
    except: pass
    return cfile

def check_proxy(f):
    '''check the proxy'''
    pr, url, ua = f
    r = requests.Session()
    r.headers._store['user-agent'] = ('User-Agent', ua)
    headers = {'User-Agent': ua}
    proxies_string = {pr[0]: pr[1]}
    timeout = 5
    try:
        res = r.get(url, headers=headers, proxies=proxies_string, timeout=timeout)
        if res.status_code == 200: 
            return (pr[0], pr[1])
    except: 
        return False

def worker_pool(input, output):
    '''run a concurent process'''
    for f in iter(input.get, 'STOP'):
        result = check_proxy(f)
        output.put(result)

def check_proxies(pr, wu, ua):
    '''run concurent processes'''
    task_queue = mp.Queue()
    done_queue = mp.Queue()
    for p in pr:
        task_queue.put((p, wu.get(), ua.get()))
    for p in pr:
        mp.Process(target=worker_pool, args=(task_queue, done_queue)).start()
    proxies = set()
    num = len(pr)
    i = 0
    while i < num:
        i += 1
        res = done_queue.get()
        if res: proxies.add(res)
    i = 0
    while i < num:
        i += 1
        task_queue.put('STOP')
    return proxies


class ua():
    l = [
        'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/73.0',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Mozilla/5.0 (X11;  Ubuntu; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-gb) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36',
        'Mozilla/5.0 (X11; Linux; rv:74.0) Gecko/20100101 Firefox/74.0',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; rv:68.7) Gecko/20100101 Firefox/68.7',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36',
        'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; ja-JP) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it-IT) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/29.0',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.13; ko; rv:1.9.1b2) Gecko/20081201 Firefox/60.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; fr-fr) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; sv-SE) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2820.59 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-HK) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
        'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.7.62 Version/11.01',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:71.0) Gecko/20100101 Firefox/71.0',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20120121 Firefox/46.0',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36',
        'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; ko-KR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F',
        'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; nb-NO) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
        'Opera/9.80 (Windows NT 6.0; U; pl) Presto/2.7.62 Version/11.01',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:62.0) Gecko/20100101 Firefox/49.0',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; es-es) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0',
        'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:10.0) Gecko/20100101 Firefox/62.0',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.59.12) Gecko/20160044 Firefox/52.59.12',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20190101 Firefox/70.0',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; ja-JP) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
        'Mozilla/5.0 (Windows NT 6.1; U; nl; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.01',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a1) Gecko/20060814 Firefox/51.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
        'Mozilla/5.0 (Windows NT 6.1; rv:27.3) Gecko/20130101 Firefox/27.3',
        'Mozilla/5.0 (Windows ME 4.9; rv:31.0) Gecko/20100101 Firefox/31.7',
        'Mozilla/5.0 (Windows NT 6.2; rv:20.0) Gecko/20121202 Firefox/26.0',
        'Mozilla/5.0 (X11; Linux ppc64le; rv:75.0) Gecko/20100101 Firefox/75.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.66.18) Gecko/20177177 Firefox/45.66.18',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:75.0) Gecko/20100101 Firefox/75.0',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-us) AppleWebKit/534.16+ (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/75.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; ar) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
        'Mozilla/5.0 (Windows; U; Windows NT 9.1; en-US; rv:12.9.1.11) Gecko/20100821 Firefox/70',
        'Mozilla/5.0 (Windows NT 5.0; Windows NT 5.1; Windows NT 6.0; Windows NT 6.1; Linux; es-VE; rv:52.9.0) Gecko/20100101 Firefox/52.9.0',
        'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:69.2.1) Gecko/20100101 Firefox/69.2',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
        'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0;  rv:11.0) like Gecko',
        'Opera/9.80 (Windows NT 6.1; WOW64; U; pt) Presto/2.10.229 Version/11.62',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
        'Mozilla/5.0 (X11; Ubuntu i686; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Mozilla/4.0 (Compatible; MSIE 8.0; Windows NT 5.2; Trident/6.0)',
        'Opera/9.80 (Windows NT 6.1; U; sv) Presto/2.7.62 Version/11.01',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 7.0; InfoPath.3; .NET CLR 3.1.40767; Trident/6.0; en-IN)',
        'Opera/9.80 (X11; Linux i686; U; ja) Presto/2.7.62 Version/11.01',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:28.0) Gecko/20100101 Firefox/31.0',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; de) Opera 11.01',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20191022 Firefox/70.0',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; cs-CZ) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; tr-TR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Mozilla/5.0 (X11; Linux i586; rv:63.0) Gecko/20100101 Firefox/63.0',
        'Opera/12.0(Windows NT 5.2;U;en)Presto/22.9.168 Version/12.00',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; de-DE) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; tr-TR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
        'Opera/9.80 (X11; Linux i686; U; es-ES) Presto/2.8.131 Version/11.11',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/58.0.1',
        'Opera/9.80 (X11; Linux x86_64; U; pl) Presto/2.7.62 Version/11.00',
        'Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0',
        'Opera/9.80 (Windows NT 6.1; Opera Tablet/15165; U; en) Presto/2.8.149 Version/11.1',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.9.168 Version/11.50',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-TW) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/58.0',
        'Opera/9.80 (Windows NT 5.1; U;) Presto/2.7.62 Version/11.01',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; de-de) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Mozilla/5.0 (X11; OpenBSD i386; rv:72.0) Gecko/20100101 Firefox/72.0',
        'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; SLCC1; .NET CLR 1.1.4322)',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.13) Gecko/20101213 Opera/9.80 (Windows NT 6.1; U; zh-tw) Presto/2.7.62 Version/11.01',
        'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16.2',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; de-DE) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; hu-HU) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
        'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:27.0) Gecko/20121011 Firefox/27.0',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Opera/9.80 (Windows NT 6.1; U; en-US) Presto/2.7.62 Version/11.01',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; sv-se) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Opera/9.80 (Windows NT 6.1; U; zh-tw) Presto/2.7.62 Version/11.01',
        'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))',
        'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.6.37 Version/11.00',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; it-it) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
        'Opera/9.80 (Windows NT 6.1; U; ko) Presto/2.7.62 Version/11.00',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
        'Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; ko-kr) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Opera/9.80 (X11; Linux i686; U; hu) Presto/2.9.168 Version/11.50',
        'Opera/9.80 (Windows NT 5.1; U; en) Presto/2.9.168 Version/11.51',
        'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
        'Opera/9.80 (X11; Linux x86_64; U; Ubuntu/10.10 (maverick); pl) Presto/2.7.62 Version/11.01',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; fr-FR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.14.1) Presto/2.12.388 Version/12.16',
        'Mozilla/5.0 (Windows ME 4.9; rv:35.0) Gecko/20100101 Firefox/35.0',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
        'Opera/9.80 (Windows NT 6.0; U; pl) Presto/2.10.229 Version/11.62',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Opera/9.80 (Windows NT 5.1; U; zh-tw) Presto/2.8.131 Version/11.10',
        'Opera/9.80 (Windows NT 6.1; U; en-GB) Presto/2.7.62 Version/11.00',
        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; de-de) AppleWebKit/534.15+ (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; de) Opera 11.51',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; fr-ch) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
        'Opera/9.80 (X11; Linux i686; U; fr) Presto/2.7.62 Version/11.01',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; ja-JP) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; zh-cn) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
        'Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00',
        'Opera/9.80 (Windows NT 6.1; U; pl) Presto/2.7.62 Version/11.00',
        'Opera/9.80 (Windows NT 6.1; U; cs) Presto/2.7.62 Version/11.01',
        'Mozilla/5.0 (Windows NT 5.1) Gecko/20100101 Firefox/14.0 Opera/12.0',
        'Opera/9.80 (Windows NT 5.1; U; cs) Presto/2.7.62 Version/11.01',
        'Opera/9.80 (X11; Linux x86_64; U; bg) Presto/2.8.131 Version/11.10',
        'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.7.62 Version/11.01',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
        'Opera/12.0(Windows NT 5.1;U;en)Presto/22.9.168 Version/12.00',
        'Mozilla/5.0 (Windows NT 6.1; U; de; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.01',
        'Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/5.0 Opera 11.11',
        'Opera/9.80 (X11; Linux i686; U; it) Presto/2.7.62 Version/11.00',
        'Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52',
        'Opera/9.80 (Windows NT 6.0; U; en) Presto/2.8.99 Version/11.10',
        'Opera/9.80 (Windows NT 6.1; U; fi) Presto/2.7.62 Version/11.00',
    ]

class ss():
    l = [
        '480x480',
        '480x576',
        '704x480',
        '720x480',
        '852x480',
        '544x576',
        '704x576',
        '720x576',
        '768x576',
        '400x270',
        '480x234',
        '480x250',
        '640x200',
        '480x272',
        '512x212',
        '512x256',
        '416x352',
        '640x240',
        '480x320',
        '640x256',
        '512x342',
        '800x240',
        '512x384',
        '640x320',
        '640x350',
        '640x360',
        '480x500',
        '720x348',
        '720x350',
        '640x400',
        '720x364',
        '800x352',
        '600x480',
        '640x480',
        '640x512',
        '768x480',
        '800x480',
        '848x480',
        '854x480',
        '800x600',
        '960x540',
        '832x624',
        '960x544',
        '1024x576',
        '1024x600',
        '960x640',
        '1024x640',
        '960x720',
        '1136x640',
        '1024x768',
        '1024x800',
        '1152x720',
        '1152x768',
        '1280x720',
        '1120x832',
        '1280x768',
        '1152x864',
        '1334x750',
        '1280x800',
        '1152x900',
        '1024x1024',
        '1366x768',
        '1280x854',
        '1600x768',
        '1280x960',
        '1080x1200',
        '1440x900',
        '1280x1024',
        '1440x960',
        '1600x900',
        '1400x1050',
        '1440x1024',
        '1440x1080',
        '1600x1024',
        '1680x1050',
        '1776x1000',
        '1600x1200',
        '1600x1280',
        '1920x1080',
        '1920x1200',
        '1920x1280',
        '2048x1152',
        '1792x1344',
        '1856x1392',
        '2880x900',
        '1800x1440',
        '2048x1280',
        '1920x1400',
        '2538x1080',
        '2560x1080',
        '1920x1440',
        '2160x1440',
        '2048x1536',
        '2304x1440',
        '2560x1440',
        '2304x1728',
        '2560x1600',
        '2560x1700',
        '2560x1800',
        '2560x1920',
        '2736x1824',
        '2880x1800',
        '2560x2048',
        '2732x2048',
        '2800x2100',
        '3200x1800',
        '3000x2000',
        '3200x2048',
        '3200x2400',
        '3440x1440',
        '3840x2160',
        '3840x2400',
        '4096x2304',
        '5120x2160',
        '4096x3072',
        '4500x3000',
        '5120x2880',
        '5120x3200',
        '5120x4096',
        '6400x4096',
        '6400x4800',
        '7680x4320',
        '7680x4800',
        '8192x4608',
        '8192x8192',
        '2048x858',
        '1998x1080',
        '1828x1332',
        '2048x1556',
        '4096x1714',
        '3996x2160',
        '4096x2160',
        '3656x2664',
        '4096x3112',
        '6144x3160',
        '5616x4096',
        '720x486',
        '1280x1080',
        '1408x1152',
        '1360x768',
    ]

class rf():
    l = [
        'https://forums.macrumors.com/',
        'https://www.dna.fi/',
        'https://yle.fi/',
        'https://airlink.worldticket.net/',
        'https://www.telia.fi/',
        'https://www.op.fi/',
        'https://www.nordea.fi/',
        'https://www.kesko.fi/',
        'https://t.co/',
        'https://stumbleupon.com/',
        'https://duckduckgo.com/',
        'https://m.facebook.com/',
        'https://www.betway787.com/',
        'https://www.retailmenot.com/',
        'https://wanelo.com/',
        'https://en.reddit.com/',
        'https://np.reddit.com/',
        'https://www.pinterest.com/',
        'https://de.reddit.com/',
        'https://fr.reddit.com/',
        'https://pay.reddit.com/',
        'https://flipboard.com/',
        'https://getpocket.com/',
        'https://i.reddit.com/',
        'https://nl.reddit.com/',
        'https://couponfollow.com/',
        'https://es.reddit.com/',
        'https://feedly.com/',
        'https://lumi.do/',
        'https://pl.reddit.com/',
        'https://re.reddit.com/',
        'https://us.reddit.com/',
        'https://viesearch.com/',
        'https://www.linkedin.com/',
        'https://www.instagram.com/',
        'https://www.europages.co.uk/',
        'https://www.europages.lt/',
        'https://hoobly.com/',
        'https://fr.pinterest.com/',
        'https://www.lightstalking.com/',
        'https://twitter.com/',
        'https://lookbook.nu/',
        'https://www.masha-sedgwick.com/',
        'https://elle-may.tumblr.com/',
        'https://preppyfashionist.com/',
        'https://lookbook.nu/forum',
        'https://www.kaboodle.com/',
        'https://www.fiverr.com/',
        'https://nordicdesign.ca/',
        'https://www.envigo.co.uk/',
        'https://www.weconnectfashion.com/',
        'https://fromhatstoheels.com/',
        'https://stylelovely.com/themidniteblues/',
        'https://vk.com/',
        'https://weheartit.com/',
        'https://aikaslovecloset.blogspot.com/',
        'https://www.amazon.com/',
        'https://www.tumblr.com/',
        'https://www.wolfandbadger.com/us/',
        'https://finlandjewelry.tumblr.com/',
        'https://www.glamourmagazine.co.uk/',
        'https://aikaslovecloset.blogspot.com/',
        'https://centurylink.net/',
        'https://www.glamour.com/fashion/welcome',
        'https://www.cosmopolitan.com/uk/',
        'https://www.dexigner.com/',
        'https://moneycortex.com/',
        'https://byruxandra.com/',
        'https://www.golfworlddestinations.com/',
        'https://weheartit.com/',
        'https://mbasic.facebook.com/',
        'https://www.producthunt.com/',
        'https://www.ssense.com/',
        'https://www.is.fi/taloussanomat/',
        'https://www.zapmeta.co.za/',
        'https://www.google.com/',
        'https://www.bing.com/',
        'https://www.facebook.com/',
        'https://www.twitter.com/',
        'https://www.reddit.com/',
    ]



# random list from fed sources
class random_list():
    '''
    list generator, returns item from the list from top and then make it as last
    '''
    def __init__(self, obj, rtype, encoding='utf-8'):
        self.update = 0
        if rtype == "file": self.list = get_file_rows(obj, encoding)
        elif rtype == "list" or rtype == "minmax": self.list = obj
    def get(self):
        if self.list:
            if self.update == 0:
                random.shuffle(self.list)
                self.update = len(self.list)
            next_row = self.list.pop(0)
            self.list.append(next_row)
            self.update -= 1
            return next_row
        else: return None
    def nextFull(self):
        if self.list:
            next_row = self.list.pop(0)
            return next_row
        else: return None
    def get_len(self):
        if self.list: return len(self.list)
        else: return None



# useragent generator
class useragents():
    '''
    user agent generator, every next UA is new
    '''
    def __init__(self, type_resource=0):
        self.ua_fake = None
        self.used = 0
        self.ua_list = []
        self.type = type_resource
        if self.type == 0: self.activate_ua()
        else: self.activate_fua()

    def get(self):
        if self.type == 0: return self.ua_list.get()
        else:
            try:
                if self.used == fake_setttings.BROWSERS_COUNT_LIMIT: self.ua_fake.update
                a = self.ua_fake.random
                self.used += 1
                return a
            except: return 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36'
    
    def activate_ua(self):
        self.ua_list = random_list(ua().l, 'list')

    def activate_fua(self):
        try:
            self.ua_fake = UserAgent(fallback='Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
            self.used = 0
        except FakeUserAgentError:
            self.activate_ua()
            self.type = 0



# screen size generator
class screensizes():
    '''screen size generator, every next screen size is new'''
    def __init__(self):
        self.l = []
        self.l = random_list(ss().l, 'list')
        self.double = []
        self.double = random_list([0,1], 'minmax')
    def get(self):
        d = self.double.get()
        if d == 0: return self.l.get()
        else: return self.generate_screensize()
    def generate_screensize(self):
        x = random.randint(650, 3500)
        y = random.randint(500, 2000)
        return f'{x}x{y}'
    # def get(self):
    #     return self.get()



# referer generator
class referers():
    '''weburl test generator, every next url is new'''
    def __init__(self):
        self.l = []
        self.l = random_list(rf().l, 'list')
    def get(self):
        return self.l.get()



# proxy generator
class proxies():
    ''' proxy generator, every next proxy is always new '''
    def __init__(self):
        self.rf = referers()
        self.u = []
        self.u = useragents()  # generate list of user agents
        self.ua = self.u.get()
        self.headers = {'User-Agent': self.ua}
        self.timeout = 10
        self.proxies = set()
        self.proxies_row = []
        self.prx = 'app.ecommaker.com'
        self.pr_key = 'be35ed15fc61579f6e620c2dc3522ffa'
        self.pr_amount = 5
        self.pr_url = f'http://{self.prx}/pr/'

    def clean(self):
        url = f'{self.pr_url}api?get=0&key={self.pr_key}'
        ua = 'prx'
        r = requests.Session()
        r.headers._store['user-agent'] = ('User-Agent', ua)
        headers = {'User-Agent': ua}
        timeout = 10
        try:
            res = r.get(url, headers=headers, timeout=timeout)
            if res.status_code != 200:
                r.close()
                return False
        except:
            r.close()
            return False
        r.close()
        return True

    def last_status(self,prms=None):
        if not prms: return False
        host = prms['host']
        port = prms['port']
        status = prms['status']

        url = f'{self.pr_url}api?h={host}&p={port}&s={status}&key={self.pr_key}'
        ua = 'prx'
        r = requests.Session()
        r.headers._store['user-agent'] = ('User-Agent', ua)
        headers = {'User-Agent': ua}
        
        try:
            res = r.post(url, headers=headers, timeout=self.timeout)
            if res.status_code != 200:
                r.close()
                return False
        except:
            r.close()
            return False

        r.close()
        return True

    def get(self, prms=None):
        if prms:
            if 'prx' in prms:
                self.prx = prms['prx']
                self.pr_url = f'http://{self.prx}/pr/'
            if 'n' in prms: self.pr_amount = prms['n']

        if not prms: prms = {'ptype': 'pr', 'check': False}

        if len(self.proxies) == 0:
            if prms:
                ptype = prms['ptype']
                check = prms['check']
                if ptype == 'default': self.get_proxies_def()
                elif ptype == 'pr': self.get_proxies_pr()  # project 'proxy'
                if check: self.proxies = check_proxies(self.proxies_row, self.rf, self.u)
                else: self.proxies = self.proxies_row
            else:
                self.get_proxies_def()
                self.proxies = check_proxies(self.proxies_row, self.rf, self.u)

        next_proxy = None

        if self.proxies: next_proxy = self.proxies.pop()
        else:
            ntimes = 10
            i = 0
            while i < ntimes:
                i += 1
                next_proxy = self.get()
                if next_proxy: return next_proxy

        return next_proxy

    def get_proxies_pr(self):
        '''return list of proxies as tuples ('https|http', 'ip:port')'''
        proxies = []
        url = f'{self.pr_url}api?get={self.pr_amount}&key={self.pr_key}'
        ua = 'prx'
        r = requests.Session()
        r.headers._store['user-agent'] = ('User-Agent', ua)
        headers = {'User-Agent': ua}
        try:
            res = r.get(url, headers=headers, timeout=self.timeout)
            if res.status_code != 200:
                r.close()
                return False
        except:
            r.close()
            return False
        
        resd = json.loads(res.text)
        r.close()

        for r in resd:
            proxies.append((r['proto'], f"{r['host']}:{r['port']}"))

        self.proxies_row = proxies

    def get_proxies_def(self):
        '''return list of proxies as tuples ('https|http', 'ip:port')'''
        proxies = []
        url = 'https://free-proxy-list.net/'
        
        # gives 300 ips at once
        res = requests.get(url, headers=self.headers)
        soup = bs(res.text, "lxml")
        for items in soup.select("tbody tr"):
            # ip = items.select("td")[0].text
            # port = items.select("td")[1].text
            # country = items.select("td")[2].text
            item_selected = items.select("td")
            if not item_selected: continue
            anonymity_flag = item_selected[4].text # 'elite proxy', 'anonimus'
            if not anonymity_flag: continue
            #if anonymity_flag != 'elite proxy': continue
            https_flag = items.select("td")[6].text # better https: 'yes'
            # if https_flag != 'yes': continue
            if https_flag == 'yes': https = 'https'
            else: https = 'http'
            proxy = ':'.join([item.text for item in items.select("td")[:2]])
            if len(proxies) <= len(self.rf.l.list):
                proxies.append((https, proxy))
            else: break
        self.proxies_row = proxies


# aliases & init
# USERAGENTS = useragents
# PROXIES = proxies
# REFERERS = referers
# SCREENSIZES = screensizes
# RANDOMSEEDS = random_list



# # check test urls
    # r = requests.Session()
    # ua = USERAGENTS.get()
    # r.headers._store['user-agent'] = ('User-Agent', ua)
    # headers = {'User-Agent': ua}
    # for url in web_test_list:
    #     try:
    #         res = r.get(url, headers=headers, timeout=5)
    #         print('.', end='', flush=True)
    #         if res.status_code != 200:  print(f'err url: {url}')
    #     except Exception as e:
    #         print(f'err url: {url} - {e}')

# #test generators
# # u = useragents()
# # s = screensizes()
# # r = referers()
# p = proxies()
# for i in range(0, 1000):
#     # print(u.get())
#     # print(s.get())
#     # print(r.get())
#     # print(p.clean())
#     pr = p.get()
#     print(pr)
#     # print(p.last_status())
#     # print(p.get({'ptype': 'pr', 'check': False}))


# if __name__ == '__main__':
#     a=1


