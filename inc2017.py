#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import csv
import re
from bs4 import BeautifulSoup
from selenium import webdriver

# URL = 'https://www.inc.com/inc5000list/json/inc5000_2016.json'
URL = 'https://www.inc.com/inc5000list/json/inc5000eu_2017.json'
FILE_DATA = 'inc5000eu_2017.csv'
YEAR = 2017

def get_data(url):
    browser = webdriver.Firefox()
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    data = json.loads(soup.find('body').text)
    browser.quit()
    return data


def get_url(data):
    list_page = [el['url'] for el in data]
    list_page = ['https://www.inc.com/profile/{}?cid=full500016-list-2'.format(el) for el in list_page]
    return list_page


def parse(data):
    browser = webdriver.Firefox()
    companies = []
    count = 0
    for com in data:
        count += 1
        try:
            id = com['id']
        except:
            id = None

        try:
            browser.get('https://www.inc.com/rest/inc5000company/{}?currentinc5000year={}'.format(com['id'], YEAR))
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            d = json.loads(soup.find('body').text)

            try:
                ceo = d['ifc_ceo_name']
            except:
                ceo = None

            try:
                revenue_s = d['current_ify_revenue']
                revenue_s = revenue_s.split()[0]
            except:
                revenue_s = None

            try:
                description = d['ifc_business_description']
                description = re.sub(r'\s+', ' ', description).replace('<p>', '').replace('</p>', '')
            except:
                description = None

            try:
                launched = d['ifc_founded']
                launched = launched.split('-')[0]
            except:
                launched = None

            try:
                site = d['ifc_url']
            except:
                site = None
        except:
            print("Id not found")
            break


        try:
            company = com['company']
        except:
            company = None

        try:
            rank = com['rank']
        except:
            rank = None

        try:
            industry = com['industry']
        except:
            industry = None

        try:
            city = com['city']
        except:
            city = None

        try:
            country = com['country']
        except:
            country = None

        try:
            url = com['url']
            url = 'https://www.inc.com/profile/{}'.format(url)
        except:
            url = None

        try:
            growth = format(round(com['growth']), ',d')
        except:
            growth = None

        try:
            revenue = format(com['revenue'], ',d')
        except:
            revenue = None
        companies.append({
            # 'id': id,
            'ceo': ceo,
            'revenue_s': revenue_s,
            # 'description': description,
            'launched': launched,
            'site': site,
            'company': company,
            'rank': rank,
            'industry': industry,
            'city': city,
            'country': country,
            'url': url,
            'growth': growth,
            'revenue': revenue,
        })
        print('Scrape: %d%%' % (count/len(data)*100))
    browser.quit()
    return companies


def save(file, companies):
    with open(file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow((
            'Rank',
            'Company',
            'URL',
            'CEO',
            'Growth, %',
            'Revenue, million',
            'Revenue',
            'City',
            'Country',
            'Industry',
            'Launched',
            # 'Description',
            'Website'
        ))

        for company in companies:
            writer.writerow((
                company['rank'],
                company['company'],
                company['url'],
                company['ceo'],
                company['growth'],
                company['revenue_s'],
                company['revenue'],
                company['city'],
                company['country'],
                company['industry'],
                company['launched'],
                # company['description'],
                company['site']
            ))


def main():
    print('Scrape START')
    print('-------------------------------')
    print('Get pages')
    data = get_data(URL)
    quantity = len(data)
    companies = parse(data)
    save(FILE_DATA, companies)
    print('Scrape 100%')
    print('-------------------------------')
    print('Scrape END')
    print('-------------------------------')
    print('Companies found: {}'.format(quantity))


if __name__ == '__main__':
    main()
