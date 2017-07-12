#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
import re
import time
import urllib.request
from bs4 import BeautifulSoup


BASE_URL = 'http://ibnet.a2zinc.net/Interbike2017/Public/exhibitors.aspx'
URL_START = 'http://ibnet.a2zinc.net/Interbike2017/Public/'
FILE = 'interbike_1.csv'


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def get_link_el(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='table table-striped table-hover')
    tr_all = table.find_all('tr')
    links = ['{}{}'.format(URL_START, tr.find('a', class_='exhibitorName')['href']) for tr in tr_all]
    booths = [tr.find('a', class_='boothLabel').get_text() for tr in tr_all]
    zipped = zip(links, booths)
    return list(zipped)


def scraping(html):
    soup = BeautifulSoup(html, 'html.parser')
    panel_body = soup.find('div', class_='panel-body')
    try:
        name = panel_body.h1.text.strip()
    except Exception:
        name = None
    try:
        city = re.sub(r'\s+', ' ', panel_body.find('span', class_='BoothContactCity').get_text()).replace(',', '').strip()
    except Exception:
        city = None
    try:
        state = re.sub(r'\s+', ' ', panel_body.find('span', class_='BoothContactState').get_text()).replace(',', '').strip()
    except Exception:
        state = None
    try:
        country = re.sub(r'\s+', ' ', panel_body.find('span', class_='BoothContactCountry').get_text()).replace(',', '').strip()
    except Exception:
        country = None
    try:
        site = panel_body.find('a', id='BoothContactUrl').get_text().strip()
    except Exception:
        site = None
    # try:
    #     booth = soup.find('ul', class_='list-inline').find_all('li')[0].text.replace('Booth:', '').strip()
    # except Exception:
    #     booth = None

    properties = {
        'name': name,
        'city': city,
        'state': state,
        'country': country,
        'site': site,
        # 'booth': booth,
    }
    return properties


def save(properties, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow((
            'Name', 'City', 'State', 'Country', 'Site', 'Booth'
        ))

        for el in properties:
            writer.writerow((
                (el['name']),
                (el['city']),
                (el['state']),
                (el['country']),
                (el['site']),
                (el['booth']),
            ))


def main():
    print('Scrape START')
    print('-------------------------------')
    booths = []
    links = get_link_el(get_html(BASE_URL))
    for link in links:
        print("Scrape:", link[0])
        # booths.append(scraping(get_html(link[0])))
        res_scrap = scraping(get_html(link[0]))
        res_scrap['booth'] = link[1]
        booths.append(res_scrap)

    save(booths, FILE)
    print('-------------------------------')
    print('All data is saved to the %s.' % FILE)
    print('Scrape END')


if __name__ == '__main__':
    main()
