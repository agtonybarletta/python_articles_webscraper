from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import logging
import urllib
from urllib.parse import urlparse


#base_url = base_url='https://www.averagesearchengine.com/search?'
base_url = base_url='https://www.google.com/search?'
lan = 'en'
blacklist_file = 'blacklist.txt'
n_articles=10

class LinkScraper:
    def __init__(self,keyword,min_date, max_date, n_articles=n_articles):
        '''

        :param keyword:
        :param min_date: mm/dd/yyyy
        :param max_date: mm/dd/yyyy
        :param n_articles:
        '''
        self.keyword= keyword
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

        # set counter to 0
        self.i = 0

        # get selenium driver with options
        options = Options()
        # keep browser close
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options)
        self.driver.get(url)
        self.links =self.driver.find_elements_by_css_selector('#rcnt div.r > a')
        return self


    def __next__(self):
        if len(self.links) <= self.i or self.i >= self.n_articles:
            raise StopIteration
        articleUrl = self.links[self.i].get_attribute('href')
        if urlparse(articleUrl).netloc not in self.blacklist:
            self.i += 1
            return articleUrl
        else:
            next(self) 

    def __close__(self):
        self.driver.close()
