#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import requests

def en_login():
    #url = 'http://m.demo.en.cx/gameengines/encounter/play/25657'
    url = 'http://m.demo.en.cx/login/signin/?return=%2f'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
    }

    UserData = {'Login': 'MrAds', 'Password': 'A4346253657'}


    #r = requests.get(url, headers = headers)
    r = requests.post(url, data=UserData, headers=headers)
    #print(r.status_code)
    #print(r.headers)

    with open('request.html', 'w') as output_file:
        output_file.write(r.text)
    pass

def en_post():
    pass