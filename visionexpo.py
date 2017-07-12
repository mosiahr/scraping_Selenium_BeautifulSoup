#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
import re
import urllib.request
from bs4 import BeautifulSoup
from random import uniform
from time import sleep
from selenium import webdriver


BASE_URL = 'http://west.visionexpo.com/exhiblist/#'
DOMEN = 'http://west.visionexpo.com'
FILE = 'visionexpo.csv'

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def get_link_driver(url):
    links = []
    driver = webdriver.Firefox()
    driver.get(url)
    sleep(5.34)
    driver.find_element_by_link_text('64').click()
    sleep(5.4)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    ul = soup.find(id='searchResultsList')
    links.extend([''.join([DOMEN, h.find('a')['href']]) for h in ul.find_all('h3', class_='name')])

    if driver.find_element_by_link_text('Next'):
        try:
            while driver.find_element_by_link_text('Next'):
                driver.find_element_by_link_text('Next').click()
                sleep(uniform(4, 6))
                soup = BeautifulSoup(driver.page_source, 'lxml')
                ul = soup.find(id='searchResultsList')
                links.extend([''.join([DOMEN, h.find('a')['href']]) for h in ul.find_all('h3', class_='name')])
        except:
            pass
    driver.quit()
    return links


def scraping(html):
    address = city = state = zip = country = tels = phone = fax = None
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find(id='pageName').text.strip()
    except Exception:
        name = None

    try:
        div = soup.find('div', class_='standDetails')
        booth = re.sub(r'\s+', '', div.find('li', class_='exhibitor').text)
    except Exception:
        booth = None

    try:
        description = soup.find('div', class_='description').text.strip()
    except Exception:
        description = None

    try:
        site = soup.find('a', class_='webAddress tracked')['href'].strip()
    except Exception:
        site = None

    try:
        address_all = soup.find('div', class_='addresses tabContent').find('div', class_='adr')
        try:
            address = address_all.find('span', class_='extended-address').text.strip()
        except Exception:
            address = None
        try:
            city = address_all.find('span', class_='locality').text.strip()
        except Exception:
            city = None
        try:
            state = address_all.find('span', class_='region').text.strip()
        except Exception:
            state = None
        try:
            zip = address_all.find('span', class_='postal-code').text.strip()
        except Exception :
            zip = None
        try:
            country = address_all.find('span', class_='country-name').text.strip()
        except Exception:
            country = None
        phone = fax = None
        try:
            tels = [re.sub(r'\s+', ' ', el.text).strip() for el in soup.find_all('div', class_='tel')]
            for el in tels:
                if re.match(r'Tel', el):
                    phone = el.split(':')[1].strip()
                if re.match(r'Fax', el):
                    fax = el.split(':')[1].strip()
        except Exception:
            pass

    except Exception:
        pass

    try:
        cat_li = soup.find('li', class_='formSection attributeattribute-dataType-categorytreenonparentselect attribute-Id-103783 attribute-Name-productsandservices twocolumn')
        categories = [
            (
                re.sub('\s+', ' ', dd.contents[0]).strip(), ', '.join([re.sub(r'\s+', ' ', li.text).strip()
                                                                       for li in dd.contents[1].find_all('li')])
         )
                for dd in cat_li.find_all('dd')
        ]
    except Exception:
        categories = None

    data = {
        'name': name,
        'booth': booth,
        'description': description,
        'site': site,
        'address': address,
        'city': city,
        'state': state,
        'zip': zip,
        'country': country,
        'phone': phone,
        'fax': fax,
        'categories': categories,
    }
    return data

def save(data, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        row_field = (
            'Name', 'Booth',
            'Company Address', 'Company City', 'Company State', 'Company Zip',  'Company Country',
            'Company phone', 'Company fax', 'Company website url', 'Description',
        )
        max_cat = 11
        row_cat = []
        for c in range(1, max_cat):
            row_cat.extend(['Category Name {}'.format(c), 'Category Sub {}'.format(c)])
        row_cat = tuple(row_cat)
        row_field = row_field + row_cat
        writer.writerow(row_field)

        for el in data:
            row = (
                (el['name']),
                (el['booth']),
                (el['address']),
                (el['city']),
                (el['state']),
                (el['zip']),
                (el['country']),
                (el['phone']),
                (el['fax']),
                (el['site']),
                (el['description']),
            )
            if el['categories']:
                for i in range(0, len(el['categories'])):
                    row = row + el['categories'][i]
            writer.writerow(row)


def main():
    print('Scrape START')
    print('-------------------------------')
    data = []
    links = get_link_driver(BASE_URL)

    for link in links:
        print("Scrape:", link)
        data.append(scraping(get_html(link)))
        sleep(uniform(1, 3))
    save(data, FILE)

    print('-------------------------------')
    print('All data is saved to the %s.' % FILE)
    print('Scrape END')

if __name__ == '__main__':
    main()
