#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re, time
import tweepy
from tweepy import OAuthHandler
from twitter_keys import *
from config import *
import logging

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

def getNews():
    config.news = [ "No Data" ]
    while True:
        raw = None; i = 2;
        if time.time() - os.path.getmtime("news.txt") < 3600:
            with open("news.txt", 'r') as f:
                temp = []
                for line in f:
                    temp.append( str(line.strip()) )
            raw = config.news = temp
            
        while raw is None:
            try:
                # Get news from twitter
                result = []
                raw = api.user_timeline(id = "cnnbrk", count = 20, include_rts = True, tweet_mode='extended' )
                # Strip url and non-latins
                for text in raw:
                    temp = ""
                    for char in  re.sub(r'https*://.+$', '', text.full_text):
                        temp += char if len( char.encode(encoding='utf_8') ) == 1 else ''
                    result.append(temp)
                    #logging.debug(result)
                # Save to file
                with open("news.txt", 'w') as file:
                    for line in result:
                        file.write(line + "\n")
                #logging.debug("File updated!!")
                # Re-direct config.news list
                config.news = result
            except Exception as e:
                #logging.debug("error occured!: " + str(e) )
                # Debugging
                if os.path.isfile("news.txt"):
                    with open("news.txt", 'r') as f:
                        temp = []
                        for line in f:
                            temp.append( str(line.strip()) )
                config.news = temp
                
                i = i ** 2; time.sleep(i)

        #logging.debug("twitter info updated!")
        #logging.debug(str(config.news))
        time.sleep(NEWS_INTERVAL)
