#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from random import choice
from time import sleep
from random import uniform


def get_html(url, useragent=None, proxy=None):
    response = requests.get(url, headers=useragent, proxies=proxy)
    return response.text

def get_ip(html):
    print('New proxy & User-Agent:')
    soup = BeautifulSoup(html, 'lxml')
    ip = soup.find('span', class_='ip').text.strip()
    ua = soup.find('span', class_='ip').find_next_sibling('span').text.strip()
    print(ip)
    print(ua)
    print('-------------------')




def main():
    url = 'http://sitespy.ru/my-ip'

    useragents = open('useragents.txt').read().split('\n')
    proxies = open('proxies.txt').read().split('\n')

    for i in range(10):
        useragent = {'User-Agent': choice(useragents)}
        proxy = {'http': 'http://{}'.format(choice(proxies))}
        try:
            html = get_html(url, useragent, proxy)
        except:
            continue
        sleep(uniform(3, 6))

        get_ip(html)

if __name__ == '__main__':
    main()