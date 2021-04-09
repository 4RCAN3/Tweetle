'''required libraries'''

import click #library for cli 
import tweepy as tw #library to access the twitter API
import os
import datetime


'''A main twitter class which is associated with various functions'''
class Twitter():

    '''creating the main attributes which will be required for accessing and authenticating the twitter api'''

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.api_key = consumer_key
        self.api_secret = consumer_secret
        self.token = access_token
        self.token_secret = access_token_secret
    
    '''creating the api object'''

    def auth(self, key, secret, token, token_secret):
        auth = tw.OAuthHandler(key, secret)
        auth.set_access_token(token, token_secret)
        api = tw.API(auth, wait_on_rate_limit=True)

        return api
    
    '''a function that returns a list of tweet objects'''

    def fetch(self, keyword, arg):
        api = self.auth(self.api_key, self.api_secret, self.token, self.token_secret)
        search_words = keyword
        tweets = tw.Cursor(api.search,
                    q=search_words,
                    lang="en").items(arg)

        return tweets
    
    '''a function that retweets using the tweet ID'''

    def retweet(self, id):
        api = self.auth(self.api_key, self.api_secret, self.token, self.token_secret)
        api.retweet(id)

    '''a function that tweets for you'''
    
    def tweet(self, arg):
        api = self.auth(self.api_key, self.api_secret, self.token, self.token_secret)
        api.update_status(status = arg)
    
    def prof(self):
        api = self.auth(self.api_key, self.api_secret, self.token, self.token_secret)
        return api.me()