# YouTube Link:

# Let's obtain the links from the following website:
# http://ingatlan.com/szukites/elado+lakas

# One of the things this website consists of is records of presidential
# briefings and statements.

# Goal: Extract all of the links on the page that point to the 
# briefings and statements.

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
#from bson.objectid import ObjectId

class IngatlanComCrawler:
    starter_url = 'http://ingatlan.com:80/szukites/elado+lakas'
    all_urls = list()
    fetched_data = list()
    http_headers = dict()

    def __init__(self, http_headers=None, starter_url = 'http://ingatlan.com:80/szukites/elado+lakas'):
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
            #house_data['_id'] = ObjectId.from_datetime(datetime.now())
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

    # TODO unfinished - just an idea for performance optimalization...
    def get_last_page_id(self, url):
        result = requests.get(url, headers=self.http_headers)
        soup = BeautifulSoup(result.content, 'lxml')
        for page_num in soup.find_all('div', class_='pagination__page-number'):
            match = re.findall(r'\/\s+([0-9]+)', str(page_num))
            if match[0] :
                print('van találat: ' + match[0])
                return int(match[0])
        return 1

    def get_all_page_urls(self):
        last_page_id = self.get_last_page_id(self.starter_url)
        all_urls = [self.starter_url + '?page=' + str(n) for n in range(1, last_page_id+1)]
        print(len(all_urls))
        return all_urls

    def fetch_all_page_urls(self):
        next_page = self.__get_next_page_button_url(self.starter_url)
        while next_page:
            self.all_urls.append(next_page)
            next_page = self.__get_next_page_button_url(next_page)
        return self.all_urls

    def crawl(self, headers=None, first_page=None, last_page=None):
        #self.all_urls = self.fetch_all_page_urls()
        self.all_urls = self.get_all_page_urls()
        if first_page is None: # fetch everything
            for url in self.all_urls:
                url_data = self.__get_house_price_data(url=url)
                self.fetched_data.extend(url_data)
        else:
            if not last_page:
                last_page = len(self.all_urls)
            last_page = min(last_page, len(self.all_urls))
            for i in range(first_page, last_page):  # fetch in range
                print('get house predict  URL: ' + self.all_urls[i])
                url_data = self.__get_house_price_data(url=self.all_urls[i])
                self.fetched_data.extend(url_data)    
        return self.fetched_data

