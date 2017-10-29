#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import csv
import re
import requests
from bs4 import BeautifulSoup

from random import choice
from random import uniform
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType

BASE = 'http://host.fieramilano.it/en/node/1857'
BASE_URL = 'http://en.expopage.net/portal/companySearchResultsIf.do?TS_ID=47&CurrentPage=1'
DOMEN = 'http://en.expopage.net/'
FILE = 'fieramilano.csv'


class Scrap:
    def __init__(self, url=None):
        self.url = url


    def get_link_driver(self, url):
        print('Getting links ...')
        links_all = []
        driver = webdriver.Firefox()
        driver.get(url)
        sleep(uniform(3, 5))

        soup = BeautifulSoup(driver.page_source, 'lxml')
        title_box = soup.find('div', class_='title_box')
        title_box = re.sub(r'\s+', ' ', title_box.text)
        title_box_list = title_box.split()

        count_company = title_box_list[0]
        count_page = int(title_box_list[7])

        for p in range(1, count_page + 1):
            print('Page: ', p)
            driver.get('http://en.expopage.net/portal/companySearchResultsIf.do?TS_ID=47&CurrentPage={}'.format(p))
            sleep(uniform(2, 5))
            soup = BeautifulSoup(driver.page_source, 'lxml')
            links = [DOMEN + a['href'] for a in soup.find_all('a', class_='testo_11_normale') if not a.contents]  # a.contents empty
            links_all.extend(links)

        driver.quit()

        return links_all

    def scraper(self, url, driver):
        print('Scraping: ', url)
        name = stand = city = country = address = phone = fax = website = email = skype = description = categories = cat_trademark = trademarks = None

        driver.get(url)
        sleep(uniform(2, 5))

        soup = BeautifulSoup(driver.page_source, 'lxml')

        try:
            name = soup.find('span', class_='tit_04_nero').text
            name = re.sub(r'\s+', ' ', name).strip()
        except:
            pass

        try:
            stand = soup.find('a', class_='eb_link_grey').text
            stand = re.sub(r'\s+', ' ', stand).strip()
        except:
            pass

        testo_bold = soup.find_all('td', class_='testo_bold_11')

        for testo in testo_bold:
            try:
                if testo.text.strip() == 'City:':
                    city_full = testo.find_next_sibling('td').text.strip().split('-')

                    city = ' '.join(city_full[:-1])
                    city = re.sub(r'\s+', ' ', city).strip()

                    country = city_full[-1]
                    country = re.sub(r'\s+', ' ', country).strip()
            except:
                pass

            try:
                if testo.text.strip() == 'Address:':
                    address = testo.find_next_sibling('td').text
                    try:
                        address = address.split('-')[:-1]
                        address = ' '.join(address)
                    except:
                        pass
                    address = re.sub(r'\s+', ' ', address).strip()
            except:
                pass

            try:
                if testo.text.strip() == 'Phone:':
                    phone = testo.find_next_sibling('td').text
                    phone = re.sub(r'\s+', ' ', phone).strip()
            except:
                pass

            try:
                if testo.text.strip() == 'Fax:':
                    fax = testo.find_next_sibling('td').text
                    fax = re.sub(r'\s+', ' ', fax).strip()
            except:
                pass

            try:
                if testo.text.strip() == 'Website:':
                    website = testo.find_next_sibling('td').text
                    website = re.sub(r'\s+', ' ', website).strip()
            except:
                pass

        testo_bold_white = soup.find_all('td', class_='testo_bold_11_white')

        for testo in testo_bold_white:
            try:
                if testo.text.strip() == 'Mail:':
                    email = testo.find_next_sibling('td').text
                    email = re.sub(r'\s+', ' ', email).strip()
            except:
                pass

            try:
                if testo.text.strip() == 'Skype:':
                    skype = testo.find_next_sibling('td').text
                    skype = re.sub(r'\s+', ' ', skype).strip()
            except:
                pass

        try:
            desc = soup.find('div', id='CP_box')
            if desc.find('table'):
                description = desc.find('table').text
                description = re.sub(r'\s+', ' ', description).strip()
        except:
            pass

        try:
            h2 = soup.find('h2', string='Product categories')
            parent_h2 = h2.parent
            categories = [re.sub(r'\s+', ' ', cat.text).strip() for cat in parent_h2.find_all('a', class_='linkato', target='_self')]
        except:
            pass

        try:
            h2 = soup.find('h2', string='Product categories')
            parent_h2 = h2.parent
            cat_trademark = [re.sub(r'\s+', ' ', cat.text).strip() for cat in parent_h2.find_all('a', class_='linkato', target='_top')]
        except:
            pass

        try:
            span = soup.find('span', string='Trademarks presented')
            parent_span = span.parent
            trademarks = [re.sub(r'\s+', ' ', cat.text).strip() for cat in parent_span.find_all('a', class_='linkato', target='_self')]
        except:
            pass

        rez = {
            'name': name,
            'url': url,
            'stand': stand,
            'city': city,
            'country': country,
            'address': address,
            'phone': phone,
            'fax': fax,
            'website': website,
            'email': email,
            'skype': skype,
            'description': description,
            'categories': categories,
            'cat_trademark': cat_trademark,
            'trademarks': trademarks,
        }

        return rez

    def save(self, prop, path):
        with open(path, 'w') as csvfile:
            writer = csv.writer(csvfile)
            row_field = (
                'Name', 'Url', 'Stand', 'City',
                'Country', 'Address', 'Phone', 'Fax',
                'Website', 'Email', 'Skype', 'Description'
            )

            max_cat = 71
            row_cat = []
            for c in range(1, max_cat):
                row_cat.extend(['Category {}'.format(c)])
            row_cat = tuple(row_cat)

            max_cat_trademark = 51
            row_cat_trademark = []
            for c in range(1, max_cat_trademark):
                row_cat_trademark.extend(['Categories of trademark {}'.format(c)])
            row_cat_trademark = tuple(row_cat_trademark)

            max_trademark = 51
            row_trademark = []
            for c in range(1, max_trademark):
                row_trademark.extend(['Trademarks {}'.format(c)])
            row_trademark = tuple(row_trademark)

            row_field = row_field + row_cat + row_cat_trademark + row_trademark
            writer.writerow(row_field)

            for el in prop:
                row = (
                    (el['name']),
                    (el['url']),
                    (el['stand']),
                    (el['city']),
                    (el['country']),
                    (el['address']),
                    (el['phone']),
                    (el['fax']),
                    (el['website']),
                    (el['email']),
                    (el['skype']),
                    (el['description']),
                )

                if el['categories']:
                    for i in range(0, len(el['categories'])):
                        row = row + (el['categories'][i],)

                if el['cat_trademark']:
                    if el['categories']:
                        for i in range(0, max_cat-len(el['categories'])-1):
                            row = row + (' ',)

                    for i in range(0, len(el['cat_trademark'])):
                        row = row + (el['cat_trademark'][i],)

                if el['trademarks']:
                    if el['categories'] and el['cat_trademark'] is None:
                        for i in range(0, max_cat-len(el['categories']) - 1):
                            row = row + (' ',)
                    elif el['categories'] is None and el['cat_trademark']:
                        for i in range(0, max_cat_trademark -len(el['cat_trademark']) - 1):
                            row = row + (' ',)
                    elif el['categories'] and el['cat_trademark']:
                        for i in range(0, max_cat_trademark - len(el['cat_trademark']) - 1):
                            row = row + (' ',)
                    for i in range(0, len(el['trademarks'])):
                        row = row + (el['trademarks'][i],)


                writer.writerow(row)


    def my_ip(self):
        # url = 'http://sitespy.ru/my-ip'
        url = 'http://whatismyipaddress.com'

        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy_type',1)
        profile.set_preference('network.proxy.http','46.235.224.235')
        profile.set_preference('network.proxy.http_port',80)
        profile.update_preferences()

        # from selenium.webdriver.common.proxy import Proxy, ProxyType
        # proxy = Proxy({
        #     'proxyType': ProxyType.MANUAL,
        #     'httpProxy': proxyStr,
        #     'ftpProxy': proxyStr,
        #     'sslProxy': proxyStr,
        #     'noProxy': '',
        #     'autodetect': False,
        # })
        # driver = webdriver.Firefox(proxy=proxy)
        driver = webdriver.Firefox(firefox_profile=profile)
        driver.get(url)
        sleep(4)
        driver.quit()


    def get_driver(self):
        proxyStr = 'http://31.173.218.199:8080'
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': proxyStr,
            'ftpProxy': proxyStr,
            'sslProxy': proxyStr,
            'noProxy': '',
        })

        driver = webdriver.Firefox(proxy=proxy)
        sleep(uniform(3, 6))
        return driver


    def run(self):
        rez = []
        print('Start ...')
        links_all = self.get_link_driver(self.url)
        print('Items: ', len(links_all))
        driver = self.get_driver()
        for link in links_all:
            rez.append(self.scraper(link, driver))

        self.save(rez, FILE)

        driver.quit()
        print('All data is saved to the %s.' % FILE)
        print('Finish.')


            # self.scraper('http://en.expopage.net//portal/standIf.do?TS_ID=47&eboothid=323185')
        # print(self.scraper('http://en.expopage.net/portal/standIf.do?TS_ID=47&eboothid=311846'))
        # rez = [self.scraper('http://en.expopage.net/portal/standIf.do?TS_ID=47&eboothid=317380')]
        # rez = [self.scraper('http://en.expopage.net/portal/standIf.do?TS_ID=47&eboothid=311846')]

        # rez = [self.scraper('http://en.expopage.net/portal/standIf.do?TS_ID=47&eboothid=303216')]
        # print(rez)
        # self.save(rez, FILE)


if __name__ == '__main__':
    scraper = Scrap(BASE_URL)
    scraper.run()
