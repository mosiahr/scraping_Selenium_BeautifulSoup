#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
import time
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from random import uniform


BASE_URL = 'http://issa17.mapyourshow.com/7_0/alphalist.cfm?alpha=*&CFID=824202&CFTOKEN=1c2b61bef65c794f-86E129EC-ABAA-96AA-7FA0508705150D58'
DOMEN = 'http://issa17.mapyourshow.com'
FILE = 'issa.csv'


def get_html(url):
    response = requests.get(url)
    return response.text


def get_link_el(url):
    driver = webdriver.Firefox()
    driver.get(url)

    try:
        endrow_el = driver.find_element_by_xpath('//*[@id="jq-myssearchresults"]/div[2]/div[4]/div[1]/h2/span')
        endrow = endrow_el.text
    except Exception:
        endrow = None

    table = driver.find_element_by_id('jq-regular-exhibitors')
    td_all = table.find_elements_by_css_selector('td.mys-align-center.mys-table-bullet')

    while len(td_all) < int(endrow):
        td_all = table.find_elements_by_css_selector('td.mys-table-exhname')
        driver.execute_script("arguments[0].scrollIntoView();", td_all[-1])
        time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    div_links = soup.find(id='jq-regular-exhibitors').find_all('td', class_='mys-table-exhname')

    links = ['{}{}'.format(DOMEN, td.a['href']) for td in div_links]
    driver.quit()
    return links


def scraping(html):
    social_facebook = social_twitter = social_linkedin = email = contact = role = phone = fax = None
    addr = country = city = state = zip = None

    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('h1', class_='sc-Exhibitor_Name').get_text().strip()
    except Exception:
        name = None
    try:
        logo_url = '{}{}'.format(DOMEN, soup.find(id='jq-exh-logo')['src'])
    except Exception:
        logo_url = None

    try:
        address = soup.find('p', class_='sc-Exhibitor_Address').contents
        address_str = []
        for el in address:    # bs4 -> str
            address_str.append(re.sub(r'\s+', ' ', el.__str__()).strip())
        try:
            address_str = ' '.join(address_str)
            address_str = address_str.split('<br/>')
            address_str = [re.sub(r'\s+', ' ', address).strip() for address in address_str]
            address_str = [address for address in address_str if address]  # remove empty el
            if len(address_str) == 4:
                address_str[0] = '{} {}'.format(address_str[0], address_str[1])
                address_str.remove(address_str[1])
            try:
                addr = address_str[0]
            except Exception:
                addr = None
            try:
                city = address_str[1].split(',')[0].strip()
            except Exception:
                city = None
            try:
                if re.search(r',', address_str[1]):
                    state_zip = address_str[1].split(',')[1].strip()
                    try:
                        state = state_zip.split()[:-1]
                        state = ' '.join(state)
                    except Exception:
                        state = None
                    try:
                        zip = state_zip.split()[-1].strip()
                    except Exception:
                        zip = None
                elif re.search(r' ', address_str[1]):
                    try:
                        city = address_str[1].split()[:-1]
                        city = ' '.join(city)
                    except Exception:
                        city = None
                    try:
                        zip = address_str[1].split()[-1].strip()
                    except Exception:
                        zip =None
            except Exception:
                pass
            try:
                country = address_str[2]
                usa = ['United States of America', 'United States']
                if country in usa:
                    country = 'USA'
            except Exception:
                country = None
        except Exception:
            pass
    except Exception:
        pass

    try:
        phone_and_fax = re.sub(r'\s+', '', soup.find('p', class_='sc-Exhibitor_PhoneFax').get_text())
        if re.search(r'P:', phone_and_fax) and re.search(r'F:', phone_and_fax):
            phone_and_fax = phone_and_fax.split('F:')
            phone = phone_and_fax[0].strip('P:')
            fax = phone_and_fax[1].strip('F:')
        elif re.search(r'P:', phone_and_fax) is None and re.search(r'F:', phone_and_fax):
            fax = phone_and_fax.strip('F:')
        elif re.search(r'F:', phone_and_fax) is None and re.search(r'P:', phone_and_fax):
            phone = phone_and_fax.strip('P:')
    except Exception:
        pass

    try:
        site = soup.find('p', class_='sc-Exhibitor_Url').a['href'].strip()
    except Exception:
        site = None

    try:
        contact_name = re.sub('\s+', ' ', soup.find('div', attrs={'style': 'padding-top:10px;'}).get_text())
        contact_name_list = contact_name.split()

        try:
            contact = contact_name_list[1:]
        except Exception:
            contact = None

        for el in contact_name_list:
            if re.search('@', el):
                try:
                    email = el   #'email': 'mattl@2xlcorp.com'
                except Exception:
                    email = None
            if re.search('Email', el):
                try:
                    cont_ind = contact_name_list.index(el)
                    contact_list = contact_name_list[1:cont_ind]  #contact': ['Matt', 'Larson', '(Sales)'
                    contact = ' '.join(contact_list) #'contact': 'Matt Larson (Sales)'

                    for cont in contact_list:
                        if re.search('\(' or '\)', cont):
                            try:
                                role_ind = contact_list.index(cont)
                                role = contact_list[role_ind].strip('\(').strip('\)')

                                contact = ' '.join(contact_list[:role_ind]).strip()  # 'contact': 'Matt Larson'
                            except Exception:
                                role = None
                except Exception:
                    contact = None
    except Exception:
        pass

    try:
        social_media = soup.find('div', class_='sc-Exhibitor_SocialMedia')
        social_links = social_media.find_all('a')
        social_links = [link['href'] for link in social_links]
    except Exception:
        social_links = None

    if social_links:
        for link in social_links:
            if re.search(r'facebook.com', link):
                social_facebook = re.search(r'facebook.com', link).string
            if re.search(r'twitter.com', link):
                social_twitter = re.search(r'twitter.com', link).string
            if re.search(r'linkedin.com', link):
                social_linkedin = re.search(r'linkedin.com', link).string
    try:
        plan_link = '{}{}'.format(DOMEN, soup.find(id='newfloorplanlink')['href'])
    except Exception:
        plan_link = None
    try:
        booth = soup.find(id='newfloorplanlink').text
        booth =booth.split('-')[-1].strip()
    except Exception:
        booth = None
    try:
        description = re.sub(r'\s+', ' ', soup.find('div', class_='mys-taper-measure').text).strip()
    except Exception:
        description = None

    brands = categories = None
    toggle = soup.find_all('a', class_='mys-vert-align-middle mys-grey jq-title')
    for el in toggle:
        if re.match(r'Brands', el.text):
            brands = [li.text for li in el.parent.find('ul', class_='mys-bullets').find_all('li')]
            brands = ', '.join(brands)
        if re.match(r'Product Categories', el.text):
            try:
                categories = [li.text for li in el.parent.find('ul', class_='mys-bullets').find_all('li')]
                categories = [(c.split('>')[0].strip(), c.split('>')[1].strip()) for c in categories]
            except Exception:
                categories = None

    properties = {
        'name': name,
        'logo_url': logo_url,
        'addr': addr,
        'city': city,
        'country': country,
        'state': state,
        'zip': zip,
        'phone': phone,
        'fax': fax,
        'site': site,
        'email': email,
        'contact': contact,
        'role': role,
        'social_facebook': social_facebook,
        'social_twitter': social_twitter,
        'social_linkedin': social_linkedin,
        'plan_link': plan_link,
        'booth': booth,
        'description': description,
        'brands': brands,
        'categories': categories,
    }
    return properties


def save(properties, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        row_field = (
            'Name', 'Booth', 'Logo Url',
            'Company Address', 'Company State', 'Company Zip', 'Company City', 'Company Country',
            'Company phone', 'Company fax', 'Company website url',
            'Email', 'Contact', 'Role', 'Facebook', 'Twitter', 'Linkedin',
            # 'PlanUrl',
            'Description', 'Brands',
        )
        max_cat = 51
        row_cat = []
        for c in range(1, max_cat):
            row_cat.extend(['Category Name {}'.format(c), 'Category Sub {}'.format(c)])
        row_cat = tuple(row_cat)
        row_field = row_field + row_cat
        writer.writerow(row_field)

        for el in properties:
            row = (
                (el['name']),
                (el['booth']),
                (el['logo_url']),
                (el['addr']),
                (el['state']),
                (el['zip']),
                (el['city']),
                (el['country']),
                (el['phone']),
                (el['fax']),
                (el['site']),
                (el['email']),
                (el['contact']),
                (el['role']),
                (el['social_facebook']),
                (el['social_twitter']),
                (el['social_linkedin']),
                # (el['plan_link']),
                (el['description']),
                (el['brands']),
            )
            if el['categories']:
                for i in range(0, len(el['categories'])):
                    row = row + el['categories'][i]
            writer.writerow(row)


def main():
    print('Scrape START')
    print('-------------------------------')
    booths = []
    links = get_link_el(BASE_URL)
    for link in links:
        time.sleep(uniform(1, 5))
        print("Scrape:", link)
        booths.append(scraping(get_html(link)))
    save(booths, FILE)
    print('-------------------------------')
    print('All data is saved to the %s.' % FILE)
    print('Scrape END')

if __name__ == '__main__':
    main()

