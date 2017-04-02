#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyvirtualdisplay import Display
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import re


BASE_URL = 'http://www.hannovermesse.de/en/exhibition/exhibitors-products/'
SITE_URL = 'http://www.hannovermesse.de'



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


def get_company(html):
	soup = BeautifulSoup(html,'html.parser')
	companies = soup.find_all('a', class_='search-link')
	companies = ['{}{}'.format(BASE_URL, el['href']) for el in companies]
	return companies


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

	# click the button: search
	browser.find_element_by_css_selector('#searchAP\:searchButton2').click()

	time.sleep(3)

	# add companies to company_pages
	company_pages.append(get_company(browser.page_source))
	print(company_pages)

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
	
	# browser.quit()
	# display.stop()	

	return company_pages


def get_html(url):
	response = urlopen(url)
	return response.read().decode('utf-8')


if __name__ == '__main__':
	print('Scrape START')
	print('-------------------------------')
	# display = Display(visible=0, size=(800, 600))
	# display.start()

	# find all countries
	# countries = find_country()
	# print(countries)

	pages_all = get_page("Italy", sector='manufacturing')
	# print(pages_all)
	# for pages in pages_all[:2]:
	# 	for page in pages:
	# 		print(page)




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
