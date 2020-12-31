###################################################################################################
###################################################################################################
### twitter_scraper.py
### Created by Wilson Woods
### 12.17.2020
### 
### Program to search and scrape tweets using twitter API
###
###################################################################################################
###################################################################################################

import tweepy
import time
import pandas as pd

class TwitterScraper:

    env = 'dev'
    search_query = ""
    result_limit = 100
    tweets_list = []
    consumer_key = "no key here, sry!"
    consumer_secret = "no key here, sry!"
    access_token = "no key here, sry!"
    access_token_secret = "no key here, sry!"



    def __init__(self, search_query, result_limit):
        self.search_query = search_query
        self.result_limit = result_limit



    def get_tweets(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth,wait_on_rate_limit=True)

        self.search_query = 'tesla'
        result_limit = 150
        try:
            tweets = tweepy.Cursor(api.search_30_day, enviroment_name=self.env,
            query=self.search_query, )
            tweets = tweepy.Cursor(api.search,q=self.search_query).items(result_limit)
            self.tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
            tweets_df = pd.DataFrame(self.tweets_list)
        
        except BaseException as ex:
            print('failed on_status,',str(ex))
            time.sleep(3)
        finally:
            return tweets_df



    def print_tweets(self):
        for n in range(0, len(self.tweets_list)):
            print('\n')
            print('Tweet created: ', self.tweets_list[n][0])
            print('\n')
            print('Tweet ID: ', self.tweets_list[n][1])
            print('\n')
            print('Tweet text: ', self.tweets_list[n][2])
            print('\n')
            print('#####################################################################')



###################################################################################################
###################################################################################################

TeslaTweets = TwitterScraper('tesla', 100)
TeslaTweets.get_tweets()
TeslaTweets.print_tweets()

###################################################################################################
###################################################################################################
