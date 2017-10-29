#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from random import choice
from time import sleep
from random import uniform


def get_html(url, useragent=None, proxy=None):
    response = requests.get(url, headers=useragent, proxies=proxy)
    print(response.status_code)
    print(response.headers['connection'])
    connection = response.headers['connection']
    return connection, response.text


def scraper(html):
    soup = BeautifulSoup(html, 'lxml')
    print(soup)


def main():
    url = 'http://en.expopage.net/portal/companySearchResultsIf.do?ACTION=CurrentPage&tbx_Search_Key=&typeSearch=exhi&Ebooth_ID=&CurrentPage=1&TS_ID=47&hid_notebookid='
    # url = 'http://host.fieramilano.it/en/node/1857'
    useragents = open('useragents.txt').read().split('\n')
    proxies = open('proxies.txt').read().split('\n')

    for i in range(10):
        sleep(uniform(3, 6))
        useragent = {'User-Agent': choice(useragents)}
        print(useragent)
        proxy = {'http': 'http://{}'.format(choice(proxies))}
        print(proxy)
        try:
            if get_html(url, useragent, proxy)[0] != 'close':
                html = get_html(url, useragent, proxy)[1]
                scraper(html)
                break
            # soup = BeautifulSoup(html, 'lxml')
            # noindex = soup.find('meta', )
            # print(html)
        except:
            continue


if __name__ == '__main__':
    main()