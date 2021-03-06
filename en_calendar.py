#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import requests
import en_request
import lxml.html as html

urls = ['http://72.en.cx/GameCalendar.aspx?t=103316&cntr=100050&zone=Real&status=Coming&p=100196',
        'http://72.en.cx/GameCalendar.aspx?t=103316&cntr=100050&zone=Points&status=Coming&p=100196']

def url_request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'}
    r = requests.post(str(url), headers=headers)
    return(r.content)


def get_games_calendar():
    result = []
    for i in urls:
        #page = html.parse(i)
        page = html.fromstring(en_request.url_request(i))
        t = page.xpath('//tr[@id[starts-with(.,"ctl18_ctl00_GamesRepeater")]]')
        for i in t:
            e = i.xpath('./td')
            date = e[4].xpath('./span/text()')[0].split('г.')[0]
            name = e[5].xpath('./a/text()')[0]
            result.append(date + "- " + name)
    return(result)


if __name__ == '__main__':
    print(get_games_calendar())