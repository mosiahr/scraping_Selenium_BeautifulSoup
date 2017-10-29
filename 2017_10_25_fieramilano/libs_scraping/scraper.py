#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import csv
import re
import sys
import urllib.request
from urllib.parse import urlparse
import requests
from requests.exceptions import MissingSchema
from bs4 import BeautifulSoup

from random import uniform
from time import sleep

BASE_URL = 'https://www.python.org/blogs'

# soup.prettify()


class Scraper:
    host = None
    host_and_scheme = None

    def __init__(self, url=None, lib_get_html='requests', lib_bs='lxml'):
        """
        :param url: url
        :param lib_get_html: 'requests', 'urllib'
        :param lib_bs: "html.parser", "lxml", "lxml-xml", "xml", "html5lib"
        """
        self._url = url
        self.lib_get_html = lib_get_html
        self.lib_bs = lib_bs
        if self._url is not None:
            self.is_connected(True)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url
        self.is_connected(True)

    @property
    def host(self):
        if self._url is not None:
            parse = urlparse(self._url)
            return parse.netloc

    @property
    def host_and_scheme(self):
        if self._url is not None:
            parse = urlparse(self._url)
            return '{}://{}'.format(parse.scheme, parse.netloc)

    def is_connected(self, write=False):
        if self._url is not None:
            try:
                ip = socket.gethostbyname(self.host)
                socket.create_connection((ip, 80), timeout=2)
                if write:
                    print('Connecting to the server ! HOST: {} | IP: {}'.format(self.host, ip))
                return True
            except Exception as e:
                print(e)
            print('Not conected !')
        print('WARNING ! url == None')
        return False

    def get_html(self, url, coding='utf-8'):
        if self.lib_get_html == 'requests':
            r = requests.get(url)
            r.encoding = coding
            print("Coding: ", r.encoding)
            return r.text
        if self.lib_get_html == 'urllib':
            r = urllib.request.urlopen(url)
            return r.read().decode(coding)

    def soup(self, url):
        """
        Returns the BeautifulSoup object
        Allows you to select the parser library.

        :return: BeautifulSoup object
        """
        try:
            if self.is_connected():
                html = self.get_html(url)
                soup = BeautifulSoup(html, self.lib_bs)
                return soup
        except MissingSchema as e:
            print(e)

    def save_csv(self, row_fields, path_to_file, mode='w'):
        with open(path_to_file, mode) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row_fields)

if __name__=='__main__':
    page = Scraper()
    page.url = BASE_URL
    print(page.url)
    print(page.host)
    print(page.host_and_scheme)

    page.save_csv(('col1', 'col2', 'col3'), 'example.csv')
