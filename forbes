#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import re
import csv
import operator
from bs4 import BeautifulSoup


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = 'https://www.forbes.com/global2000/list/#tab:overall'
URL_JSON = 'https://www.forbes.com/ajax/list/data?year=2016&uri=global2000&type=organization'
FILE = 'forbes_global2000.csv'
FILE_PAGES = 'forbes_pages.csv'


def get_html(url):
    response = requests.get(url)
    return response.text


def get_data(url):
    response = requests.get(url).json()
    return response

def get_url(data):
    list_page = [el['uri'] for el in data]
    list_page = ['https://www.forbes.com/companies/{}/'.format(el) for el in list_page]
    return list_page


def save_img(src, name):
    dir_img = '{}/{}_img'.format(BASE_DIR, 'forbes')
    if not os.path.exists(dir_img):
        os.mkdir(dir_img)

    try:
        r = requests.get(src)
        if r.status_code == 200:
            with open("{}/{}.jpg".format(dir_img, name), 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        else:
            print('Status code:', r.status_code)
    except ConnectionError as err:
        print(err)


def parse(data):
    companies = []
    founded = website = employees = city = description = marketValue = uri_page = None
    count = 0
    for company in data:
        count += 1
        print("Parse: {} company".format(count))
        try:
            rank = company['rank']
        except:
            rank = None

        try:
            uri = company['uri']

            html = get_html('https://www.forbes.com/companies/{}/'.format(uri))
            soup = BeautifulSoup(html, 'html.parser')

            try:
                uri_page = 'https://www.forbes.com/companies/{}/'.format(uri)
            except:
                uri_page = None

            try:
                founded = soup.find('dt', text='Founded').findNext('dd').get_text()
            except:
                founded = None

            try:
                website = soup.find('dt', text='Website').findNext('dd').get_text()
            except:
                website = None

            try:
                employees = soup.find('dt', text='Employees').findNext('dd').get_text()
            except:
                employees = None

            try:
                city = soup.find('dt', text='Headquarters').findNext('dd').get_text()
                city = city.split(',')[0]
            except:
                city = None

            try:
                sales = soup.find('dt', text='Sales').findNext('dd').get_text()
                # sales = city.split()[0]
            except:
                sales = None

            try:
                description = soup.find('div', class_='profile').get_text()
                description = re.sub(r'\s+', ' ', description).strip()
            except:
                description = None

            try:
                marketValue = soup.find('li', class_='amount').text
                marketValue = marketValue.split()[0]
            except:
                marketValue = None

        except:
            uri = None

        try:
            name = company['name']
        except:
            name = None

        try:
            imageUri = 'https://images.forbes.com/media/lists/companies/{}_416x416.jpg'.format(company['imageUri'])
            save_img(imageUri, name)
        except:
            imageUri = None

        try:
            industry = company['industry']
        except:
            industry = None

        try:
            country = company['country']
        except:
            country = None

        try:
            headquarters = company['headquarters']
        except:
            headquarters = None

        try:
            state = company['state']
        except:
            state = None

        try:
            ceo = company['ceo']
        except:
            ceo = None

        companies.append({
            'rank': rank,
            'uri': uri_page,
            'name': name,
            'industry': industry,
            'country': country,
            # 'sales': sales,
            'marketValue': marketValue,
            'headquarters': headquarters,
            'state': state,
            'ceo': ceo,
            'imageUri': imageUri,

            'founded': founded,
            'website': website,
            'employees': employees,
            'city': city,
            'description': description,
        })

    companies.sort(key=operator.itemgetter('rank'))
    return companies


def save(file, companies):
    with open(file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow((
            'Rank',
            'Name',
            'URL',
            'Industry',
            'Country',
            'Market Value, b',
            'Headquarters',
            'CEO',
            'Founded',
            'Website',
            'Employees',
            'Sales',
            'City',
            'State',
            'Description'
        ))

        for company in companies:
            writer.writerow((
                company['rank'],
                company['name'],
                company['uri'],
                company['industry'],
                company['country'],
                company['marketValue'],
                company['headquarters'],
                company['ceo'],
                company['founded'],
                company['website'],
                company['employees'],
                company['sales'],
                company['city'],
                company['state'],
                company['description']
            ))


def main():
    print('Scrape START')
    print('-------------------------------')
    print('Get pages')
    data = get_data(URL_JSON)
    print("Find {} companies".format(len(data)))
    save(FILE, parse(data))
    print('Scrape 100%')
    print('-------------------------------')
    print('Scrape END')


if __name__ == '__main__':
    main()


