# -*- coding: utf-8 -*-


import os
import csv

from fake_useragent import UserAgent, settings as fake_setttings
from fake_useragent import FakeUserAgentError



# https://pypi.org/project/fake-useragent/

 
# dump file to save osm results in
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
dump_folder = __location__ + '\\'



def main():
    l = []  # final list of emails


    with open(dump_folder + 'ua.csv', 'r', encoding='utf-8') as f:
        l = f.readlines()


    ua_fake = UserAgent(fallback='Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
    ua_fake.update()
    used = 0

    num = 5000
    i = 0
    while i < num:
        i += 1

        ua = ua_fake.random

        ua_check = ua.lower()
        if (
            ua+'\n' in l
            or 'bot' in ua_check
            or 'spider' in ua_check
            or 'google' in ua_check
            or 'baidu' in ua_check
            or 'crawler' in ua_check
            or 'iphone' in ua_check
            or 'ipad' in ua_check
            or 'android' in ua_check
        ): continue
        
        
        if used == fake_setttings.BROWSERS_COUNT_LIMIT: ua_fake.update
        used += 1
        
        l.append(ua+'\n')



    with open(dump_folder + 'ua.csv', 'w', encoding='utf-8') as f:
        f.writelines(l)







if __name__ == "__main__":
    main()


