#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import requests

def url_request(url, login = None, password = None):

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
    }

    if login is None and password is None:
        r = requests.get(url, headers = headers)
    else:
        UserData = {'Login': login, 'Password': password}
        r = requests.post(url, data=UserData, headers=headers)
    return(r.content)
