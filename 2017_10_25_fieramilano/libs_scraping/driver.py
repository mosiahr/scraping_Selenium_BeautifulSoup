#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import csv
import re
import urllib.request
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from random import uniform
from time import sleep
from selenium import webdriver

def driver_decorator(func):
    def wrapper(url, *args,  quit=True, **kwargs):
        driver = webdriver.Firefox()
        driver.get(url)
        sleep(uniform(2, 3))
        func(url, driver=driver, *args, **kwargs)
        if quit:
            driver.quit()
    return wrapper