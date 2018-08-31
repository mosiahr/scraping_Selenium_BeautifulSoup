import re
import csv
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from libscrap import Scraper

# from random import choice
from random import uniform
from time import sleep

BASE_URL = 'https://exhibitors.exporeal.net/prj_840/view/index.cfm?nv=1.2&lng=2'
FILE = 'exporeal.csv'
FIELDS = ('Url', 'Name', 'Address', 'City', 'Country', 'Phone', 'Email', 'Website')


class Scrap(Scraper):
    def __init__(self, *args, **kwargs):
        super(Scrap, self).__init__(*args, **kwargs)
        self.driver = webdriver.Firefox()
        self.scrap(url=self.url)

    def scrap(self, url):
        self.driver.get(url)
        sleep(uniform(2, 3))
        self.save_csv(FIELDS, FILE)
        self.driver.find_element_by_xpath('//*[@id="jl_websitearea"]/div[2]/div[1]/form[1]/div/div[1]/div/div[1]/input[3]').click()
        sleep(uniform(2, 4))

        input_el = self.driver.find_element_by_id('changenumbertxt_paging_1')
        input_el.clear()
        input_el.send_keys("31")
        input_el.send_keys(Keys.RETURN)
        sleep(uniform(2, 4))

        while True:
            next = self.driver.find_element_by_xpath('//*[@id="jl_websitearea"]/div[2]/div[1]/form[2]/div/div[2]/div/div[2]/div/div/div[3]/input')
            try:

                links_driver = self.driver.find_elements_by_css_selector('div.jl_lexname a')
                links_page = [link.get_attribute('href') for link in links_driver[1:]]

                for url in links_page:
                    data = self.scrap_company(url)
                    self.save_one_row(data, FILE)

                next.click()
                sleep(uniform(4, 6))

            except:
                break
        self.driver.quit()

    def scrap_company(self, url):
        s = self.soup(url)
        print('Scrap: ', url)

        name = address = city = country = phone = email = website = None
        sectors = []

        for info in s.find_all('div', class_='jl_exd_facts'):
            try:
               name = info.find(id='exdetails').text.strip()
            except:
                name = None

            try:
                address = info.find('div', class_='jl_adr_strasse').text.strip()
            except:
                address = None

            try:
                city = info.find('div', class_='jl_adr_ort').text
                city = re.findall(r'[^0-9\-]+', city)[0].strip()
            except:
                city = None

            try:
                country = info.find('div', class_='jl_adr_land').text.strip()
            except:
                country = None

            try:
                phone = info.find('div', class_='adr_phone').text
                phone = re.findall(r'[0-9\-\+\s]+', phone)[0].strip()
            except:
                phone = None

            try:
                email = info.find('div', class_='view_kontakt_mail').a['href']
                email = re.findall(r'mailto:\s*(.*)', email)[0].strip()
            except:
                email = None

            try:
                website = info.find('div', class_='view_kontakt_url').a['href'].strip()
            except:
                website = None

        try:
            for el in s.find_all('div', class_='jl_dtprodarea'):
                for a in el.find_all('a'):
                    sector = re.sub(r'\s+', ' ', a.text).strip()
                    sectors.append(sector)
        except:
            sectors = None

        return {
            'url': url,
            'name': name,
            'address': address,
            'city': city,
            'country': country,
            'phone': phone,
            'email': email,
            'website': website,
            'sectors': sectors,
        }

    def save_one_row(self, data, path):
        with open(path, 'a') as csvfile:
            writer = csv.writer(csvfile)
            row = (
                (data['url']),
                (data['name']),
                (data['address']),
                (data['city']),
                (data['country']),
                (data['phone']),
                (data['email']),
                (data['website']),
            )
            if data['sectors'] is not None:
                for i in range(0, len(data['sectors'])):
                    row = row + (data['sectors'][i],)
            writer.writerow(row)


if __name__ == '__main__':
    start = time.time()
    scraper = Scrap(BASE_URL)
    print("Time run: ", time.time() - start)
