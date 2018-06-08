#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, re, time
import urllib.request
from xml.dom.minidom import parseString
import logging

import json

from weather_keys import *
#from config import *


import urllib, json
baseurl = "https://query.yahooapis.com/v1/public/yql?"
#yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='boston, ma')"
woeid = 2495739
woeid = 15015439
yql_query = "select * from weather.forecast where woeid=" + str(woeid)
yql_url = baseurl + urllib.parse.urlencode({'q':yql_query}) + "&format=json"
result = urllib.request.urlopen(yql_url).read().decode('utf8')
data = json.loads(result)

#print (data['query']['results']['channel'])
# condition
base = data['query']['results']['channel']['item']
condition = base['condition']
icon = "weather/" + condition['code'] + ".gif"
if not os.path.isfile(icon):
    try: 
        icon_url = re.search('\"(http://[^\"]*)\"', base['description'])
        if icon_url:
            hoge = urllib.request.urlretrieve( icon_url.group(1), icon )
            print("icon saved.")
    except Exception as e:
        logging.debug("cannot download image file!")

print (json.dumps(data, indent=4, sort_keys=True))
#print (base['description'])









"""
location = "MA/Cambridge.json"
url = "http://api.wunderground.com/api/" + wunderground_key +"/conditions/q/" + location

connection = urllib.request.urlopen(
    "http://api.openweathermap.org/data/2.5/forecast?q=Boston,USA&units=metric&mode=xml&APPID=" +
    weather_key )
raw = connection.read().decode('utf8')
connection.close()

xml = parseString(raw)
#print(xml.toprettyxml())
print( [ node.getAttributeNode("from").nodeValue for node in xml.getElementsByTagName("time") ] )
"""
"""
print(str(xml))
for item in xml:
    print (item)
"""
"""
#print (str(raw))
myjson  = json.loads(raw)
#raw (json.dumps(myjson, indent=4, sort_keys=True))
print(myjson.keys())
for item in myjson["list"]:
    for key, item in item.items():
        print (key, item)
    print()
"""        
#print( myjson["list"] )
#print (str(raw))
#print(myjson["city"]["name"])
#print (myjson["coord"])
#logging.debug(str(raw))
"""
def getNews():
    config.news = [ "No Data" ]
    while True:
        raw = None; i = 4;
        while raw is None:
            try:
                raw = api.user_timeline(id = "cnnbrk", count = 10, include_rts = True )
            except Exception as e:
                logging.debug("error occured!: " + str(e) )
                i = i ** 2; time.sleep(i)
        config.news = [ re.sub(r'https*://.+$', '', status.text) for status in raw ]
        time.sleep(NEWS_INTERVAL)

"""
