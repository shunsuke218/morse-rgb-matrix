#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, time, random
import urllib.request
import logging
import json
from weather_keys import *
from config import *
import urllib, json


base_url = "http://dataservice.accuweather.com/forecasts/v1/daily/1day/"
query = "?language=en-US&details=true&apikey="

class Config():
    def __init__(self):
        self.weather = {}

    
def getWeather(config, location):

    def FtoC(input):
        return round( ((input - 32) * 5.0/9.0), 0)

    #weather_key = "hogehoge!"
    #config = Config()
    #config.weather = {}
    config.weather = {}
    url = base_url + str(location) + query + weather_key
    logging.debug("Starting getWeather")
    while True:
        temp = {};
        i = 2; result = None
        t = time.time()
        if os.path.isfile(str(location) + ".json") and \
           time.time() - os.path.getmtime(str(location) + ".json") < WEATHER_INTERVAL:
            logging.debug(str(location) + ": The file already exists!")
            with open(str(location) + ".json", 'r') as f:
                result = f.read()
        while not result:
            logging.debug("No File found for weather!")
            try:
                time.sleep(random.randint(2,10))
                result = urllib.request.urlopen(url).read().decode('utf8')
                t = time.time()
                with open (str(location) + ".json", 'w') as f:
                    f.write(result)
                logging.debug("Weather info updated!!")
            except Exception as e:
                logging.debug("error occured!: " + str(e))
                #print("error occured!: " + str(e))
                i = i **2; time.sleep(i)
                #if time.time() - t > 14400: # No update for 4hrs
                #    config.weather = {}

            
        data = json.loads(result)

        # Headline
        temp["headline"] = data["Headline"]["Text"]
        temp["time"] = data["Headline"]["EffectiveDate"]
        temp["time"] = temp["time"][:-3] + temp["time"][-2:]

        # DailyForecasts
        forecasts = data["DailyForecasts"][0]

        #     - Sun
        data_sun = forecasts["Sun"]
        temp["rise"] = int(data_sun["EpochRise"])
        temp["set"] = int(data_sun["EpochSet"])

        #     - Temperature
        data_tempe = forecasts["Temperature"]
        #         - Minimum
        minf = int(data_tempe["Minimum"]["Value"])
        temp["min"] = (minf, FtoC(minf))
        #         - Maximum
        maxf = int(data_tempe["Maximum"]["Value"])
        temp["max"] = (maxf, FtoC(maxf))

        #     - RealFeelTemperature
        data_rftempe = forecasts["RealFeelTemperature"]
        #         - Minimum
        minf = int(data_rftempe["Minimum"]["Value"])
        temp["rfmin"] = (minf, FtoC(minf))
        #         - Maximum
        maxf = int(data_rftempe["Maximum"]["Value"])
        temp["rfmax"] = (maxf, FtoC(maxf))

        #     - Day
        data_day = forecasts["Day"]
        temp["dicon"] = data_day["Icon"]
        temp["dphrase"] = data_day["LongPhrase"]
        temp["dpreciption"] = data_day["PrecipitationProbability"]
        
        #     - Night
        data_day = forecasts["Night"]
        temp["nicon"] = data_day["Icon"]
        temp["nphrase"] = data_day["LongPhrase"]
        temp["npreciption"] = data_day["PrecipitationProbability"]

        # Re-link config.weather
        config.weather[location] = temp 

        logging.debug("weather info updated: " + str(config.weather))

        # Sleep
        time.sleep(WEATHER_INTERVAL)
        #time.sleep(5)
        
if __name__ == '__main__':
    getWeather(338668)
