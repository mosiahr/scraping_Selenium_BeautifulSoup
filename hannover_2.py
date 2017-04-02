#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
FILE = 'x_csv_hannover_scrape2.csv'
# FILE = 'x_hannover_scrape2.xlsx'

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
	# print(len(comp))
	return comp


def get_page(country, sector):
	company_pages = []

	# display = Display(visible=0, size=(800, 600))
	# display.start()

	browser = webdriver.Firefox()  # Your browser will open, Python might ask for permission
	browser.get(BASE_URL) 

	browser.execute_script("document.getElementById('searchAP\:j_idt107').style.display='block';")
	browser.find_element_by_css_selector('#searchAP\:j_idt107').click()

	browser.find_elements_by_xpath("//*[contains(text(), 'European Union')]")[0].click()

	browser.find_elements_by_xpath("//*[contains(text(), '{}')]".format(country))[0].click()

	# open show all
	show_all = browser.find_elements_by_css_selector('.toggleLimited')
	show_all[2].click()

	if sector == 'manufacturing':
		# change cheack box style by display: block
		browser.execute_script("document.getElementById('searchAP\:zb\:35\:r').style.display='block';")

		# click the Manufacturing industry
		browser.find_element_by_css_selector('#searchAP\:zb\:35\:r').click()

	elif sector == 'transportation':
		# change cheack box style by display: block
		browser.execute_script("document.getElementById('searchAP\:zb\:289\:r').style.display='block';")

		time.sleep(3)

		print(browser.find_element_by_css_selector('#searchAP\:zb\:289\:r'))

		# click the Transportation and storage
		browser.find_element_by_css_selector('#searchAP\:zb\:289\:r').click()

	elif sector == 'construction':
		# change cheack box style by display: block
		browser.execute_script("document.getElementById('searchAP\:zb\:237\:r').style.display='block';")

		# click the Transportation and storage
		browser.find_element_by_css_selector('#searchAP\:zb\:237\:r').click()


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

	# browser.quit()
	# display.stop()	

	return company_pages

def parse(html, sector):
	soup = BeautifulSoup(html,'html.parser')
	companies = []

	try:
		name = soup.find('h1', itemprop='name')
		name = name.get_text()
	except:
		name = None

	try:
		website = soup.find('a', class_="textLink icon-external-link")
		website = website['href']
	except:
		website = None

	companies.append({
		'name': name,
		'website': website,
		'sector': sector,
	})
	
	return companies


# def save(file, companies):
# 	wb = Workbook()

# 	std = wb.get_sheet_by_name('Sheet')
# 	wb.remove_sheet(std)

# 	ws1 = wb.create_sheet('Italy')

# 	header = ['Name', 'Website', 'Sector']
# 	max_col = 3
# 	for col in range(1, max_col+1):
# 		ws1.cell(row=1, column=col, value=header[col-1])

# 	row_max = len(companies)
# 	row_max_ind = row_max + 2
# 	print(row_max)
# 	print(row_max_ind)

# 	for row in range(2, row_max_ind):
# 		comps = [companies[row-2]['name'], companies[row-2]['website'], companies[row-2]['sector']]
# 		# print(comps)
# 		for col in range(1, max_col+1):
# 			ws1.cell(row=row, column=col, value=comps[col-1])

# 	# print(companies[0])
# 	# last_col = row_max

# 	wb.save(file)

def save_country(file, companies):
	'''	Save single country file ''' 

	with open(path_file, 'a') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(('Name', 'Website', 'Sector'))

		for company in companies:
			writer.writerow((company['name'], company['website'], company['sector']))
		


def main(country, sector):

	companies = []
	
	# for sector in sectors:
	# 	print(sector)


	# pages_all = get_page("Italy", sector='manufacturing')
	pages_all = get_page(country, sector)
	# print(pages_all)
	for pages in pages_all:
		for page in pages:
			# print(page)
			companies.extend(parse(get_html(page), sector=sector))
			# print(companies)

	print(companies)
	save(FILE, companies)


if __name__ == '__main__':
	print('Scrape START')
	print('-------------------------------')
	# display = Display(visible=0, size=(800, 600))
	# display.start()

	# find all countries
	# countries = find_country()
	# print(countries)

	# main(country='Italy', sector='manufacturing')
	main(country='Italy', sector='transportation')


	


	# browser = webdriver.Firefox()  # Your browser will open, Python might ask for permission
	# browser.get(URL)  





		# print(browser.get_window_position())
		# browser.execute_script("window.scrollTo(0, 1200)")

		# elem = browser.find_element_by_class_name('<strong>European Union</strong>')
		# elem = browser.find_element_by_class_name('level1')

		# print(elem)
		# elem.click()

		# driver.find_element_by_xpath("html/body/div[2]/div[4]/div/div[5]/div/div/div/div[1]/div/div[2]/div[1]/ol/li[3]/ol/li[1]/div/div[2]/h3/a").click()
		# driver.find_elements_by_xpath("//*[contains(text(), 'portnovschool')]")

		# el = browser.find_elements_by_xpath("html/body/page-wrapper/")
	# browser.execute_script("document.getElementById('searchAP\:j_idt107').style.display='block';")
	# browser.find_element_by_css_selector('#searchAP\:j_idt107').click()
	# 	 time.sleep(3)


	# browser.find_elements_by_xpath("//*[contains(text(), 'European Union')]")[0].click()

	

	# browser.find_elements_by_xpath("//*[contains(text(), '{}')]".format(country))[0].click()


		# time.sleep(3)
		# show_all = browser.find_element_by_link_text("Show all")
		# browser.find_elements_by_xpath("//*[contains(text(), 'Show all')]")[0].click()


		# browser.execute_script("window.scrollTo(0, 100)")

	# open show all
	# show_all = browser.find_elements_by_css_selector('.toggleLimited')
	# show_all[2].click()

	# # change cheack box style by display: block
	# browser.execute_script("document.getElementById('searchAP\:zb\:35\:r').style.display='block';")
	# cheack_box = browser.find_element_by_css_selector('#searchAP\:zb\:35\:r')
	# cheack_box.click()

	# search_button = browser.find_element_by_css_selector('#searchAP\:searchButton2')
	# search_button.click()

		# browser.execute_script("window.scrollTo(0, 1600)")
		# search = search.find_elements_by_xpath(".//span")[0]
		# search = search.find_element_by_xpath("./div[0]")
		# search = search.find_element_by_class_name('checkBox')
		# search = search.find_element_by_css_selector('.filter')
		# search.find_element_by_class_name()



		# browser.quit()
		# display.stop()
