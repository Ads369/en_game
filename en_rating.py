#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import requests
import en_request
import lxml.html as html

urls = ['56877']


def get_info_game():
    result = []
    for i in urls:
        page = html.fromstring(en_request.url_request(
                'http://72.en.cx/GameDetails.aspx?gid=%s' %i))
        name = page.xpath('//a[@id="lnkGameTitle"][1]/text()')[0]
        quality = page.xpath('//*[@id="GameDetail_lnkGameQuality"][1]'
                                '/text()')[0]
        print(name)
        print(quality)

        authors = page.xpath('//a[@id[starts-with(.,"GameDetail_AuthorsRepeater_ct")]]')
        for y in authors:
            print(i.text)

        teams = page.xpath('//a[@id[starts-with(.,"top10Winners_SingleRepeater_ctl")]'
            ' and contains(@href,"TeamDetails")]')
        for y in range(0,len(teams)):
            print(i+1)
            print(teams[i].xpath('./@href')[0].split('=')[1])
            print(teams[i].text)

    return(result)


def get_info_players():
    result = []
    for i in urls:
        page = html.fromstring(en_request.url_request(
                'http://72.en.cx/GameWinnerMembers.aspx?gid=%s' %i))
        teams = page.xpath('//a[contains(@id,"_lnkCaptain")]')
        print(len(teams))
        for j in range(0,len(teams)):
            print(j+1)
            number = j*2
            if len(str(number)) == 2:
                number = str(number)
            else:
                number = '0' + str(number)
            players = page.xpath(
                    '//a[contains(@id,"WinnersRepeater_ctl%s")]' %str(number))
            for x in players:
                print(x.text)
            print('----')
    return(result)



if __name__ == '__main__':
    print(get_info_players())