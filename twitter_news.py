#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
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

        # Debugging

        if os.path.isfile("news.txt"):
            with open("news.txt", 'r') as f:
                for line in f:
                    #config.news.append(line.strip().encode('utf8', 'ignore')) if line is not None else ""
                    config.news.append(str(line.strip()).encode('utf8', 'ignore'))

        config.news = config.news[1:]
        '''
        while raw is None:
            try:
                raw = api.user_timeline(id = "cnnbrk", count = 10, include_rts = True )
                config.news = [ re.sub(r'https*://.+$', '', status.text) for status in raw ]
            except Exception as e:
                logging.debug("error occured!: " + str(e) )
                i = i ** 2; time.sleep(i)
        '''


        logging.debug("twitter info updated!")
        logging.debug(str(config.news))
        time.sleep(NEWS_INTERVAL)
