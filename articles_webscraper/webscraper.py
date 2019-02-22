from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import logging
import urllib
from urllib.parse import urlparse

class SearchEngineArticles:
    def __init__(self,keyword,base_url='https://www.averagesearchengine.com/seach?',min_date=None, max_date=None, n_articles=10, lan='en', blacklist_file='blacklist.txt'):
        '''

        :param keyword:
        :param min_date: mm/dd/yyyy
        :param max_date: mm/dd/yyyy
        :param n_articles:
        :param len:
        '''
        self.keyword = keyword
        self.min_date = min_date
        self.max_date = max_date
        self.n_articles = n_articles
        self.lan = lan
        self.base_url = base_url
        #load blacklist file
        with open(blacklist_file) as bl:
            blacklist = bl.readlines()
        blacklist = [line.rstrip('\n') for line in blacklist]
        self.blacklist = blacklist
    def __iter__(self):

        url = self.base_url 
        query = urllib.parse.quote_plus(self.keyword)
        url += 'q='+query
        url += '&hl='+self.lan
        #add date range if specified
        if self.min_date is not None and self.max_date is not None:
            url += '&tbs=cdr:1,cd_min:{0},cd_max:{1}'.format(self.min_date, self.max_date)
        #add num article if specified
        url+= '&num='+str(self.n_articles)
        self.search_engine_url = url
        self.l = []
        options = Options()
        options.add_argument('--headless')
        parsed = 0
        driver = webdriver.Firefox(options=options)
        driver.get(self.search_engine_url)
        time.sleep(1)
        for a in driver.find_elements_by_xpath('//div[@class="r"]/a'):
            link = a.get_attribute('href')
            print('linkoooooooooooooooooooo',link)
            network_location = urlparse(link).netloc
            if network_location not in self.blacklist:
                self.l.append(link)
                parsed +=1
                if parsed == self.n_articles:
                    break
        driver.close()
        self.index = 0
        return self

    def __next__(self):
        if self.index == len(self.l):
            raise StopIteration
        else:
            ret = self.l[self.index]
            self.index += 1

            return ret
