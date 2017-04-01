#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyvirtualdisplay import Display
from selenium import webdriver
import time

URL = 'http://www.hannovermesse.de/en/exhibition/exhibitors-products/'

# display = Display(visible=0, size=(800, 600))
# display.start()

browser = webdriver.Firefox()  # Your browser will open, Python might ask for permission
browser.get(URL)  

# print(browser.get_window_position())
# browser.execute_script("window.scrollTo(0, 1200)")

# elem = browser.find_element_by_class_name('<strong>European Union</strong>')
# elem = browser.find_element_by_class_name('level1')

# print(elem)
# elem.click()

# driver.find_element_by_xpath("html/body/div[2]/div[4]/div/div[5]/div/div/div/div[1]/div/div[2]/div[1]/ol/li[3]/ol/li[1]/div/div[2]/h3/a").click()
# driver.find_elements_by_xpath("//*[contains(text(), 'portnovschool')]")

# el = browser.find_elements_by_xpath("html/body/page-wrapper/")
browser.execute_script("document.getElementById('searchAP\:j_idt107').style.display='block';")
browser.find_element_by_css_selector('#searchAP\:j_idt107').click()
time.sleep(3)


browser.find_elements_by_xpath("//*[contains(text(), 'European Union')]")[0].click()
browser.find_elements_by_xpath("//*[contains(text(), 'Italy')]")[0].click()

# time.sleep(3)
# show_all = browser.find_element_by_link_text("Show all")
# browser.find_elements_by_xpath("//*[contains(text(), 'Show all')]")[0].click()


# browser.execute_script("window.scrollTo(0, 100)")

# open show all
show_all = browser.find_elements_by_css_selector('.toggleLimited')
show_all[2].click()

# change cheack box style by display: block
browser.execute_script("document.getElementById('searchAP\:zb\:35\:r').style.display='block';")
cheack_box = browser.find_element_by_css_selector('#searchAP\:zb\:35\:r')
cheack_box.click()

search_button = browser.find_element_by_css_selector('#searchAP\:searchButton2')
search_button.click()

# browser.execute_script("document.getElementByName('#searchAP\:zb\:35\:r').style.display='block';")


# search = search.find_element_by_class_name("filter")
# search = search.find_elements_by_xpath("span")[0]

# browser.execute_script("window.scrollTo(0, 1600)")

# search = search.find_elements_by_xpath(".//span")[0]




# print(search)

# search.click()

# search.click()
# search = search.find_element_by_xpath("./div[0]")
# search = search.find_element_by_class_name('checkBox')
# search = search.find_element_by_css_selector('.filter')
# search.find_element_by_class_name()


# print(type(show_all))
# print(show_all)


# browser.quit()


# display.stop()
