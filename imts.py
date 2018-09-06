import requests
import re
import csv
from urllib.parse import urlparse
from urllib.parse import parse_qs
from time import sleep
from random import uniform

from bs4 import BeautifulSoup
from selenium import webdriver

URL_GET_COUNTRIES = 'https://www.imts.com/exhdir/ajax/ajaxfunctions.cfm?mysAJaxCall=getCountries&avoidcache=1535839013390'
DOMEN = 'https://www.imts.com'
FILE = 'imts.csv'
FIELDS = (
    'Url', 'Name', 'Address', 'City', 'Country', 'Phone', 'Website', 'Booth', 'Url booth',
    'Category', 'SubCategory',
    'Category', 'SubCategory',
    'Category', 'SubCategory',
    'Category', 'SubCategory',
    'Category', 'SubCategory',
    'Category', 'SubCategory',
    'Category', 'SubCategory',
    'Category', 'SubCategory',
    'Category', 'SubCategory',
    'Category', 'SubCategory',
    'Category', 'SubCategory',
    'Category', 'SubCategory',
    'Category', 'SubCategory',
    'Category', 'SubCategory',
    'Category', 'SubCategory',
    'Category', 'SubCategory',
)


class Scrap:
    def __init__(self):
        self.scrap()

    def get_html(self, url, data={}):
        response = requests.get(url, data)
        print("Status: ", response.status_code)
        return response.text

    def get_resp_decode(self, url, data={}):
        """ JSON to dict """
        response = requests.get(url, data)
        print("Status: ", response.status_code)
        return response.json()

    def get_countries(self, url):
        countries = self.get_resp_decode(url)
        countries = countries['DATA']['DATA']
        countries = [k for k, v in countries]
        countries.sort()
        return countries

    def scrap(self):
        # Save field name
        self.save_csv(FIELDS, FILE)

        # Get companies
        countries = self.get_countries(URL_GET_COUNTRIES)

        for c in countries:
            print("----------- Scraping country: {} ---------".format(c))
            driver = webdriver.Firefox()
            url = "https://www.imts.com/exhdir/search.cfm?" \
                "advsrch-country={}&advsrch=true&advsrch-showresults=true".format(c)
            driver.get(url)
            sleep(uniform(5, 6))

            # Scroll into link last
            while True:
                count_before = driver.find_elements_by_css_selector('#jq-regular-exhibitors td.mys-table-exhname a').__len__()
                driver.execute_script("var links = document.querySelectorAll('td.mys-table-exhname a');"
                                      "links[links.length-1].scrollIntoView(top=false);"
                                      )
                sleep(uniform(4, 5))
                count_after = driver.find_elements_by_css_selector('#jq-regular-exhibitors td.mys-table-exhname a').__len__()
                if count_before == count_after:
                    break

            # Get company links
            try:
                company_links = [(el.get_attribute('href'), el.text) for el in
                                 driver.find_elements_by_css_selector('#jq-regular-exhibitors td.mys-table-exhname a')]
            except:
                company_links = None

            # Scraping company
            if company_links is not None:
                for link, name in company_links:
                    print("Scraping: ", link)
                    html = self.get_html(link)
                    # print(link.text)
                    rez_row = self.scrap_item(html, link, name)
                    # print(rez_row)
                    self.save_one_row(rez_row, FILE)
            driver.close()

    def scrap_item(self, html, url, name):
        soup = BeautifulSoup(html, 'lxml')

        try:
            address = soup.find('p', class_='sc-Exhibitor_Address').__str__().split('<br/>')
            address = [re.sub(r'<.*>', ' ', addr) for addr in address]
            address = [re.sub(r'\s+', ' ', addr) for addr in address]
            address = [addr.strip() for addr in address]
            address = [addr for addr in address if addr != '']
            try:
                if (len(address) > 3):
                    addr = (address[0] + ' ' + address[1]).strip()
                else:
                    addr = address[0].strip()
            except:
                addr = None

            try:
                if ',' in address[-2]:
                    city = address[-2].split(',')[0]
                else:
                    city = re.findall(r'[A-Za-z\-\s]+', address[-2])[0].strip()
                # city = re.sub(r'[A-Z][A-Z]', '', city).strip().strip(',')
            except Exception as e:
                print(e)
                city = None

            try:
                country = address[-1]
            except:
                country = None
        except:
            addr = None
            city = None
            country = None

        try:
            phone = soup.find('p', class_='sc-Exhibitor_PhoneFax').text
            phone = re.findall(r'P:\s+[0-9\-\s+]+', phone)[0]
            phone = phone.replace('P:', '').strip()
        except:
            phone = None
        try:
            website = re.sub(r'\s+', ' ', soup.find('p', class_='sc-Exhibitor_Url').text).strip()
        except:
            website = None

        try:
            url_booth = re.sub(r'\s+', ' ', soup.find(id='newfloorplanlink')['href']).strip()
            booth = urlparse(url_booth).query
            booth = parse_qs(booth)['booth'][0]
        except:
            url_booth = None
            booth = None

        try:
            categories = soup.find('strong', text=re.compile(r'Product Categories'))
            categories = categories.find_parent().find_parent()
            categories = categories.find('ul', class_='mys-bullets').find_all('li')
            categories = [li.text for li in categories]
            categories = [el.split('>') for el in categories]
        except Exception as e:
            print("Error categories: ", e)
            categories = None

        return {
            'url': url,
            'name': name,
            'addr': addr,
            'city': city,
            'country': country,
            'phone': phone,
            'website': website,
            'booth': booth,
            'url_booth': DOMEN + url_booth,
            'categories': categories,
        }

    def save_csv(self, row_fields, path_to_file, mode='w'):
        with open(path_to_file, mode) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row_fields)

    def save_one_row(self, data, path):
        with open(path, 'a') as csvfile:
            writer = csv.writer(csvfile)
            row = (
                (data['url']),
                (data['name']),
                (data['addr']),
                (data['city']),
                (data['country']),
                (data['phone']),
                (data['website']),
                (data['booth']),
                (data['url_booth']),
            )

            if data['categories'] is not None:
                for i in range(0, len(data['categories'])):
                    row += (data['categories'][i][0], data['categories'][i][1])
            writer.writerow(row)


if __name__ == '__main__':
    scrap = Scrap()
