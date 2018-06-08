#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re, time
import tweepy
from tweepy import OAuthHandler
from twitter_keys import *
from config import *

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

def getNews():
    config.news = [ "No Data" ]
    while True:
        raw = None; i = 2;
        while raw is None:
            try:
                raw = api.user_timeline(id = "cnnbrk", count = 10, include_rts = True )
            except Exception as e:
                logging.debug("error occured!: " + str(e) )
                i = i ** 2; time.sleep(i)
        config.news = [ re.sub(r'https*://.+$', '', status.text) for status in raw ]
        time.sleep(NEWS_INTERVAL)
