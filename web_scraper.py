###################################################################################################
###################################################################################################
### web_scraper.py
### Created by Wilson Woods
### 12.16.2020
### 
### Program to scrape and summarize news articles from news.google.com
### Articles can be searched given a search query and the time interval (in days)
### in which to search
### Result is a dictionary/dataframe containing a url, title, date/time, and summary 
### of every parsable article yielded in the initial search
###
###################################################################################################
###################################################################################################

import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import urllib.parse
from urllib.parse import urlparse
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from gensim.summarization import summarize
from collections import namedtuple



class WebScraper:

    search_query = ""
    time_frame = 1
    result_limit = 10
    status = 100
    source = ""
    base_url = 'https://news.google.com'
    url = 'https://news.google.com/search?q={}%20when%3A{}d&hl=en-US&gl=US&ceid=US%3Aen'
    resulting_articles= {'title': [], 'url': [], 'date_time': [], 'summary':[]}
    key_words = []
    key_word_counts = {}



    def __init__(self, search_query, time_frame, result_limit):
        self.search_query = search_query
        self.time_frame = time_frame
        self.result_limit = result_limit



    ### find_result_page()
    ### access the google news results page based on search query and time frame
    ### returns text of results page that has been auto-scrolled to 
    ### provide a sufficient number of results
    def find_result_page(self):
        self.url = self.url.format(self.search_query, self.time_frame)
        try:
            driver = webdriver.Chrome()
            driver.get(self.url)
        except Exception as ex:
            print(str(ex))
        time.sleep(1)
        control_elem = driver.find_element_by_tag_name("body")
        scroll_down = int((self.result_limit / 10) + 1)

        while scroll_down:
            control_elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
            scroll_down-=1
        self.source = driver.page_source



    ### find_articles()
    ### locate article titles, urls, and times, save these in resulting_articles dict
    ### returns the dict with title, url, and date_time lists populated
    def find_articles(self):
        html = requests.get(self.url)
        self.status = html.status_code
        print('HTML Status: {}'.format(self.status))

        if html.status_code == 200:
            results_page = BeautifulSoup(self.source, 'html.parser')
            titles = results_page.find_all('h3')
            post_times = results_page.find_all('time')
            index = 0
            for index, title in enumerate(titles):
                self.resulting_articles['title'].append(title.text)
                article_url = self.base_url + title.contents[0].get('href')[1:]
                self.resulting_articles['url'].append(article_url)
                if index == self.result_limit - 1:
                    break
            index = 0
            for index, post_time in enumerate(post_times):
                self.resulting_articles['date_time'].append(post_time.get('datetime'))
                if index == len(self.resulting_articles['url']):
                    break
        else:
            print('Error accessing search results')



    ### get_article_summaries()
    ### follows each link found by find_articles(), parses the article
    ### from the html, and summarizes the article to roughly 30% (ratio=0.3)
    ### of its initial size using gensim.summarization
    ### returns the dict with 'summary' list populated
    def get_article_summaries(self):
        for _ in range(0, len(self.resulting_articles['url'])):
            self.resulting_articles['summary'].append('None')

        for n in range(0, len(self.resulting_articles['url'])):
            article_url = self.resulting_articles['url'][n]
            try:
                article_page = requests.get(article_url).text
            except Exception as ex:
                print(str(ex))

            parsed_html = BeautifulSoup(article_page, 'html.parser')
            #if parsed_html.find('h1'):
            #    headline = parsed_html.find('h1').get_text()
            #else:
            #    headline = 'Could not retrieve headline'
            if parsed_html.find_all('p'):
                p_tags = parsed_html.find_all('p')
                p_tags_text = [tag.get_text().strip() for tag in p_tags]
                sentences = [sentence for sentence in p_tags_text if not '\n' in sentence]
                sentences = [sentence for sentence in sentences if '.' in sentence]
                if len(sentences) > 1:
                    parsed_article = ' '.join(sentences)
                    summary = summarize(parsed_article, ratio=0.3)
                elif len(sentences) == 1:
                    summary = sentences[0]
                else:
                    summary = "Failed to parse article, no summary created"
            else:
                summary = "Failed to parse article, no summary created"
            self.resulting_articles['summary'][n] = summary



    ### print_article_summaries()
    ### print contents of resulting_articles dict
    def print_article_summaries(self):
        for n in range(0, len(self.resulting_articles['url'])):
            print('\n')
            print(self.resulting_articles['title'][n])
            print('\n')
            print(self.resulting_articles['date_time'][n])
            print('\n')
            print(self.resulting_articles['url'][n])
            print('\n')
            print(self.resulting_articles['summary'][n])
            print('\n')
            print('#########################################################################')



###################################################################################################
###################################################################################################

Tesla = WebScraper("tesla", "1", 10)
Tesla.find_result_page()
Tesla.find_articles()
Tesla.get_article_summaries()
Tesla.print_article_summaries()
print('Complete!')

###################################################################################################
###################################################################################################
