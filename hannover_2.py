#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pyvirtualdisplay import Display
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
from openpyxl import Workbook
import csv
import time
import re


BASE_URL = 'http://www.hannovermesse.de/en/exhibition/exhibitors-products/'
SITE_URL = 'http://www.hannovermesse.de'
FILE = 'hannovermesse_scrape2.xlsx'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


sectors = [
		'Manufacturing industry',
		'Construction/construction industry',
		'Transportation and storage',
		'Information and communication',
		'Human health and social work activities',
	]


def find_country():
	''' find all country '''
	display = Display(visible=0, size=(800, 600))
	display.start()
	browser = webdriver.Firefox()  # Your browser will open, Python might ask for permission
	browser.get(BASE_URL) 
	browser.execute_script("document.getElementById('searchAP\:j_idt107').style.display='block';")
	browser.find_element_by_css_selector('#searchAP\:j_idt107').click()
	browser.find_elements_by_xpath("//*[contains(text(), 'European Union')]")[0].click()

	soup = BeautifulSoup(browser.page_source,'html.parser')
	countries = soup.find_all('div', class_='checkBox expander')[3]
	countries = countries.next_sibling.get_text()
	countries = countries.split('\n\n\n\n')
	countries = [re.sub(r'\s+', ' ', country).strip()  for country in countries]

	browser.quit()
	display.stop()		
	return countries


def get_html(url):
	response = urlopen(url)
	return response.read().decode('utf-8')


def get_company(html):
	comp = []
	soup = BeautifulSoup(html,'html.parser')
	companies = soup.find_all('a', class_='search-link')
	companies = ['{}{}'.format(SITE_URL, el['href']) for el in companies]
	for company in companies:
		if company not in comp:
			comp.append(company)
	return comp


def get_page(country, sector):
	company_pages = []

	display = Display(visible=0, size=(800, 600))
	display.start()

	browser = webdriver.Firefox()  # Your browser will open, Python might ask for permission
	browser.get(BASE_URL) 

	browser.execute_script("document.getElementById('searchAP\:j_idt107').style.display='block';")
	browser.find_element_by_css_selector('#searchAP\:j_idt107').click()

	browser.find_elements_by_xpath("//*[contains(text(), 'European Union')]")[0].click()

	browser.find_elements_by_xpath("//*[contains(text(), '{}')]".format(country))[0].click()

	# open show all
	show_all = browser.find_elements_by_css_selector('.toggleLimited')
	show_all[2].click()

	if sector == sectors[0]:
		# change cheack box style by display: block
		browser.execute_script("document.getElementById('searchAP\:zb\:35\:r').style.display='block';")

		# click the Manufacturing industry
		browser.find_element_by_css_selector('#searchAP\:zb\:35\:r').click()

	elif sector == sectors[1]:
		# change cheack box style by display: block
		browser.execute_script("document.getElementById('searchAP\:zb\:237\:r').style.display='block';")

		# click the Construction/construction industry
		browser.find_element_by_css_selector('#searchAP\:zb\:237\:r').click()

	elif sector == sectors[2]:
		# change cheack box style by display: block
		browser.execute_script("document.getElementById('searchAP\:zb\:289\:r').style.display='block';")

		# click the Transportation and storage
		browser.find_element_by_css_selector('#searchAP\:zb\:289\:r').click()

	elif sector == sectors[3]:
		# change cheack box style by display: block
		browser.execute_script("document.getElementById('searchAP\:zb\:316\:r').style.display='block';")

		# click the Information and communication
		browser.find_element_by_css_selector('#searchAP\:zb\:316\:r').click()

	elif sector == sectors[4]:
		# change cheack box style by display: block
		browser.execute_script("document.getElementById('searchAP\:zb\:405\:r').style.display='block';")

		# click the Human health and social work activities
		browser.find_element_by_css_selector('#searchAP\:zb\:405\:r').click()

	# click the button: search
	browser.find_element_by_css_selector('#searchAP\:searchButton2').click()

	time.sleep(3)

	# add companies to company_pages
	company_pages.append(get_company(browser.page_source))

	try: 
		paginator = browser.find_element_by_css_selector('.pagination-list')
		last_page = paginator.find_elements_by_xpath('li')[-1:]
		last_page = last_page[0].text

		for page in range(1, int(last_page)):
			# click the button next-page
			button_next_page = browser.find_element_by_css_selector('a.button:nth-child(3)')
			button_next_page.click()
			time.sleep(5)
			# add companies to company_pages
			company_pages.append(get_company(browser.page_source))
	except :
		pass

	browser.quit()
	display.stop()	

	return company_pages

def parse(html, sector):
	soup = BeautifulSoup(html,'html.parser')
	companies = []

	try:
		name = soup.find('h1', itemprop='name')
		name = name.get_text().replace(';', '')
	except:
		name = None

	try:
		website = soup.find('a', class_="textLink icon-external-link")
		website = website['href'].replace(';', '')
	except:
		website = None

	companies.append({
		'name': name,
		'website': website,
		'sector': sector,
	})
	return companies


def save_country(file, companies):
	'''	Save single country file ''' 

	with open(file, 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(('Name', 'Website', 'Sector'))

		for company in companies:
			writer.writerow((company['name'], company['website'], company['sector']))
		

def csv_to_xlsx(file, worksheet):
	with open(file, 'r') as f:
		for row in csv.reader(f):
			worksheet.append(row)


def save_csv_to_xlsx():
	wb = Workbook()

	std = wb.get_sheet_by_name('Sheet')
	wb.remove_sheet(std)

	files = os.listdir("companies/")
	files.sort()
	worksheet = [wb.create_sheet(file[:-4]) for file in files]

	for i in range(0, len(files)):
		csv_to_xlsx('./companies/{}'.format(files[i]), worksheet[i])	

	wb.save(FILE)


def main():
	print('Scrape START')
	print('-------------------------------')
	# create directory
	dir_companies = BASE_DIR + "/companies"
	if not os.path.exists(dir_companies):
	    os.mkdir(dir_companies)

	# find country
	print("SOURCE COUNTRIES")
	countries = find_country()
	count = 0
	for country in countries:
		print("SOURCE:", country)
		companies = []
		for sector in sectors:
			pages_all = get_page(country, sector)
			for pages in pages_all:
				for page in pages:
					print("ADD page: % s" % page)
					companies.extend(parse(get_html(page), sector))
					count += 1

		companies.sort(key=lambda k : k['name'])
		save_country(dir_companies + '/' + country + '.csv', companies)
	save_csv_to_xlsx()
	print('Scrape 100%')
	print('-------------------------------')
	print('Scrape END')
	print('-------------------------------')
	print('Companies found: {}'.format(count))


if __name__ == '__main__':
	main()