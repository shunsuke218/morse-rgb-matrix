#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import threading, time
from datetime import datetime, timezone
from time import strftime
import pytz
from itertools import cycle

from twitter_news import *
from weather import *
from config import *
# Local class
#from weather import *
#from stock import *

# TODO: Create extended classes based on Content class
class Content:
    # Will be overrode
    def __init__(self):
        self.content = ""
        self.width = 0; self.height = 0
        self.x = 0
        self.sizechangeable = False; self.sizeupdated = False
        self.ypadding = 0;

    def move(self, num=1):
        self.x -= num

    def setx(self, x):
        self.x = x
        
    def draw(self, x, y, draw):
        return

    def maxheight(self, y):
        padding = int(( y - self.height )/2)
        self.ypadding = padding if padding > 0 else 0
        return

class TextContent(Content):
    def __init__(self, text = None, offset=0):
        Content.__init__(self)
        self.font = NEWSFONT
        self.text = text or ""
        self.width, self.height = self.font.getsize(self.text)
        self.offset = offset

    def draw(self, x, y, draw):
        #
        #logging.debug("x,y: " + str(x) + "," +  str(y) + " xd,yd: " + str(x + self.width) + "," + str(y + self.height) + ", width: " + str(self.width))
        # If content out of boundry, don't do anything
        if ( x > WIDTH or x + self.width < 0 ): return
        # If content inside the matrix, delete the old one and draw
        draw.text( (x, y + self.offset), self.text, font=self.font, fill=GREY )
        #draw.text( (x, y), self.text, font=self.font, fill=GREY )

class NewsContent(Content):
    def __init__(self, config, odd=False, font=NEWSFONT):
        Content.__init__(self)
        self.sizechangeable = True;
        self.config = config
        self.font = font
        self.odd = int(odd)
        texts = None
        while not texts:
            texts = config.news[self.odd:][::2]
            time.sleep(.5)
        #logging.debug( "starting newscontents: " + str(id(self)) + str(texts) )
        self.texts = cycle( texts )
        self.text = str(next(self.texts)).upper() + " |  "
        self.width, self.height = self.font.getsize(self.text)

        # Start thread to update content this object
        self.thread = threading.Thread(target=self.update)
        self.thread.daemon = True
        self.thread.start()
        
    def setx(self, x):
        # Update text if reached left-edge
        #logging.debug("!!!self.x + self.width <= 0!!!: " + str(self.x + self.width))
        self.text = next(self.texts).upper() + "  |  "
        self.sizeupdated = True
        self.x = x
        
    def draw(self, x, y, draw):
        # If content out of boundry, don't do anything
        if ( x > WIDTH or x + self.width < 0 ): return

        #logging.debug(str(id(self)) + ": drawing...: " + str(self.text))
        #logging.debug("x,y: " + str(x) + "," +  str(y) + " xd,yd: " + str(x + self.width) + "," + str(y + self.height) + ", height, width: " + str(self.width) + "," + str(self.width) )

        # If content inside the matrix, delete the old one and draw
        draw.text( (x, y), self.text, font=self.font, fill=GREY )

    def update(self):
        while True:
            if config.news is not self.config.news:
                self.texts = cycle(config.news[self.odd:][::2])
            time.sleep(300)
        
    
class TimeContent(Content):
    def __init__(self, location=None, font=TIMEFONT):
        Content.__init__(self)
        self.font = font
        if not location:
            self.timezone = datetime.now( timezone.utc ) \
                                .astimezone().tzinfo
            self.loc = "BOS"
        elif location is "Japan":
            self.timezone = pytz.timezone('Asia/Tokyo')
            self.loc = "TYO"
        elif location is "France":
            self.timezone = pytz.timezone('Europe/Paris')
            self.loc = "FRA"

        # Start thread to update time each second
        self.thread = threading.Thread(target=self.update)
        self.thread.daemon = True
        self.time = ""; self.width = 0; self.height = 0
        self.thread.start()
    
    def update(self):
        while True:
            self.time = datetime.now(self.timezone).strftime(self.loc + " %H:%M:%S %Z | ")
            self.width, self.height = self.font.getsize(self.time)
            time.sleep(.5)
        
    def draw(self, x, y, draw):
        # If content out of boundry, don't do anything
        if ( x > WIDTH or x + self.width < 0 ): return
        draw.text( (x, y), self.time, font=self.font, fill=WHITE )
        
class WeatherTracker(object):
    # Track running thread/location to avoid multiple
    notrunning = {}
tracker = WeatherTracker()

class WeatherContent(Content):
    def __init__(self, config, location=None, offset = 0):
        if tracker.notrunning.get(location, True):
            weatherThread = threading.Thread(target=getWeather, args=(config, location))
            weatherThread.daemon = True
            weatherThread.name = "weather_" + str(location)
            weatherThread.start()
            tracker.notrunning[location] = False
        
        Content.__init__(self)
        # variable
        self.config = config
        self.weather = self.config.weather
        self.icon = Image.open("weather/0.png", 'r')
        self.sizechangeable = True; self.sizeupdated = False
        self.xspace = 1; self.yspace = 1
        self.location = location
        self.low = (0,0); self.high = (0,0)
        
        # Calculate size
        self.calcsize()

        # Start thread to update content this object
        self.thread = threading.Thread(target=self.update)
        self.thread.daemon = True
        self.thread.start()
        time.sleep(1)


    def calcsize(self):
        self.width = self.icon.size[0]
        self.height = self.icon.size[1]

        self.tempechigh = [
            (str(self.high[1]),NEWSFONT, DARKRED),
            (" C",NEWSFONT, GREY)
        ]
        self.tempefhigh = [
            (str(self.high[0]),NEWSFONT, DARKRED),
            (" F",NEWSFONT, GREY)
        ]
        self.tempeclow = [
            (str(self.low[1]),NEWSFONT, DARKBLUE),
            (" C",NEWSFONT, GREY)
        ]
        self.tempeflow = [
            (str(self.low[0]),NEWSFONT, DARKBLUE),
            (" F",NEWSFONT, GREY)
        ]

        def addcol(self, high, low):
            highsize = [ info[1].getsize(info[0]) for info in high ]
            maxhighx = sum([ temp[0] for temp in highsize]) + self.xspace * len(high)
            maxhighy = max( highsize, key=lambda x:x[1] )[1]
            highsize = (maxhighx, maxhighy)

            lowsize = [ info[1].getsize(info[0]) for info in low ]
            maxlowx = sum([ temp[0] for temp in lowsize ]) + self.xspace * len(low)
            maxlowy = max(lowsize, key=lambda x:x[1])[1]
            lowsize = (maxlowx, maxlowy)

            self.width += max(maxhighx, maxlowx) + self.xspace
            self.height = max(self.height, maxhighy + maxlowy)

            return highsize, lowsize

        self.highsizec, self.lowsizec = addcol(self, self.tempechigh, self.tempeclow)
        self.highsizef, self.lowsizef = addcol(self, self.tempefhigh, self.tempeflow)
        """
        for each in [(self.tempechigh, self.tempeclow), (self.tempefhigh, self.tempeflow)]:
            tempehighsize = [ info[1].getsize(info[0]) for info in each[0] ]
            maxhighx = sum([ temp[0] for temp in tempehighsize]) + self.xspace * len(each[0])
            maxhighy = max( tempehighsize, key=lambda x:x[1] )[1]
            self.highsize = (maxhighx, maxhighy)

            tempelowsize = [ info[1].getsize(info[0]) for info in each[1] ]
            maxlowx = sum([ temp[0] for temp in tempelowsize ]) + self.xspace * len(each[1])
            maxlowy = max(tempelowsize, key=lambda x:x[1])[1]
            self.lowsize = (maxlowx, maxlowy)

            self.width += max(maxhighx, maxlowx) + self.xspace
            self.height = max(self.height, maxhighy + maxlowy)
        """
        
    def update(self, feel=False ):
        location = self.location
        while True:
            timewait = WEATHER_INTERVAL
            if self.weather is not None and \
               self.weather.get(location) is not None and \
               self.weather.get(location).get("headline") is not None:
                # Weather information exists
                myweather = self.weather.get(location)
                logging.debug(str(myweather))
                # Get headline
                self.headline = myweather["headline"]
                t = datetime.strptime(myweather["time"], "%Y-%m-%dT%H:%M:%S%z").timestamp()

                # Check if it's day/night
                day = True if t >= myweather["rise"] \
                      and t <= myweather["set"] else False
                # Select phrase & correct icon
                self.phrase = myweather["dphrase"] if day else myweather["nphrase"]
                iconnum = myweather["dicon"] if day else myweather["nicon"]
                icon = "weather/" + str(iconnum) + ".png"
                if not os.path.isfile(icon): icon = "weather/0.png"
                # Get temperature info
                self.high = myweather["min"] if not feel else myweather["rfmin"]
                self.low = myweather["max"] if not feel else myweather["rfmax"]
            else:
                self.headline = self.phrase = "N/A"
                icon = "weather/0.png"
                self.high = self.low = (0, 0)
                timewait = 1

            logging.debug(str(location) + ": " + icon)
            self.icon = Image.open(icon, 'r')
            self.icon.thumbnail((32,32))

            # Update config
            self.weather = self.config.weather
            self.calcsize()

            self.sizeupdated = True
            time.sleep(timewait)

    def draw(self, x, y, draw):
        #logging.debug("drawing weather...")
        #logging.debug("self.weather: " + str(self.weather))
        #logging.debug(" width, height: (" + str(self.width) + ", " + str(self.height) + ")" )

        xspace = self.xspace; yspace = self.xspace
            
        def printRight(x,y,input,pfont, pcolor):
            draw.text((x,y), str(input), font=pfont, fill=pcolor)
            return pfont.getsize(input)[0] + xspace
        
        # Icon
        widthicon = self.icon.size[0]; heighticon = self.icon.size[1]
        try:
            if self.icon is not None:
                config.image.paste(self.icon, (x, y + self.ypadding))
        except SyntaxError:
            logging.error("Error!")
            logging.error("location: " + str(self.location))
            logging.error("weather: " + str(self.weather))
        except AttributeError:
            logging.error("Error!")
            logging.error("location: " + str(self.location))
            logging.error("weather: " + str(self.weather))
            
            #logging.debug("height:" + str(heighticon))

        # Max C
        xoffset = x + widthicon + xspace
        yoffset = y - 2
        for each in self.tempechigh:
            #logging.debug("each in self.tempechigh: " + str(each))
            temp = printRight(xoffset, yoffset, each[0], each[1], each[2])
            xoffset += temp

        # Min C
        xoffset = x + widthicon + xspace
        yoffset = y + self.highsizec[1] + yspace - 6
        for each in self.tempeclow:
            #logging.debug("each in self.tempeclow: " + str(each))
            temp = printRight(xoffset, yoffset, each[0], each[1], each[2])
            xoffset += temp

        cwidth = max(self.highsizec[0], self.lowsizec[0])
        
        # Max F
        xoffset = x + widthicon + cwidth + xspace
        yoffset = y - 2
        for each in self.tempefhigh:
            #logging.debug("each in self.tempechigh: " + str(each))
            temp = printRight(xoffset, yoffset, each[0], each[1], each[2])
            xoffset += temp

        # Min F
        xoffset = x + widthicon + cwidth + xspace
        yoffset = y + self.highsizef[1] + yspace - 6
        for each in self.tempeflow:
            #logging.debug("each in self.tempeclow: " + str(each))
            temp = printRight(xoffset, yoffset, each[0], each[1], each[2])
            xoffset += temp
 

