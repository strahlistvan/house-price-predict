# YouTube Link:

# Let's obtain the links from the following website:
# https://ingatlan.com/szukites/elado+lakas

# One of the things this website consists of is records of presidential
# briefings and statements.

# Goal: Extract all of the links on the page that point to the 
# briefings and statements.

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

class IngatlanComCrawler:
    starter_url = 'https://ingatlan.com/szukites/elado+lakas'
    all_urls = list()
    fetched_data = list()
    http_headers = dict()

    def __init__(self, http_headers=None, starter_url = 'https://ingatlan.com/szukites/elado+lakas'):
        if http_headers != None:
            self.http_headers = http_headers
        self.starter_url = starter_url

    def __get_key_from_tag(self, tag):
        tag = str(tag)
        if not tag:
            return 'other'
        match = re.search('--[^\"]+', tag)
        if match:
            key = match.group()[2:]
            return key
        return 'other'

    def __convert_to_number(self, price_str, multiplier=1):
        price_str = str(price_str)
        match = re.search('[\d|\.]+', price_str)
        if match:
            return float(match.group())*multiplier
        return 0

    def __get_house_price_data(self, url):
        house_data_list = list()
        result = requests.get(url, headers=self.http_headers)

        soup = BeautifulSoup(result.content, 'lxml')

        for list_link in soup.find_all('div', class_='listing__card'):
            house_data = dict()
            house_data['data_source'] = url
            house_data['fetch_date'] = datetime.now()

            price = list_link.find('div', class_='price').string
            house_data['price'] = self.__convert_to_number(price, 1000000)
            address = list_link.find('div', class_='listing__address')
            if address:
                house_data['address'] = address.string

            listing_pars = list_link.find('div', class_='listing__parameters')
            for par in listing_pars:
                key = self.__get_key_from_tag(par)
                value =str(par.string)
                if key in ['room-count', 'area-size', 'balcony-size']:
                    value= self.__convert_to_number(value)
                house_data[key] = value
            house_data_list.append(house_data)
        return house_data_list

    def __get_next_page_button_url(self, url):
        result = requests.get(url, headers=self.http_headers)
        soup = BeautifulSoup(result.content, 'lxml')

        for buttons in soup.find_all('a', class_='pagination__button'):
            if buttons.string == 'Következő oldal':
                return buttons['href']
        return None

    def fetch_all_page_urls(self):
        next_page = self.__get_next_page_button_url(self.starter_url)
        while next_page:
            self.all_urls.append(next_page)
            next_page = self.__get_next_page_button_url(next_page)
        return self.all_urls

    def crawl(self, headers=None):
        print('crawler is running')
        self.fetch_all_page_urls()
        for url in self.all_urls:
            print(url)
            url_data = self.__get_house_price_data(url=url)
            self.fetched_data.extend(url_data)
        #print(self.fetched_data)
        return self.fetched_data


