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

    def move(self, num=1):
        self.x -= num

    def setx(self, x):
        self.x = x
        
    def draw(self, x, y, draw):
        return

class HogeContent(Content):
    def __init__(self, height=0):
        Content.__init__(self)
        self.text = "hoge"
        self.width, self.height = FONT7.getsize(self.text)

    def draw(self, x, y, draw):
        #logging.debug("drawing...: " + self.text)
        #logging.debug("x,y: " + str(x) + "," +  str(y) + " xd,yd: " + str(x + self.width) + "," + str(y + self.height) + ", width: " + str(self.width))
        # If content out of boundry, don't do anything
        if ( x > WIDTH or x + self.width < 0 ): return
        # If content inside the matrix, delete the old one and draw
        draw.text( (x, y), self.text, font=FONT7, fill=(110, 110, 110) )

class NewsContent(Content):
    def __init__(self, config, odd=False):
        Content.__init__(self)
        self.sizechangeable = True;
        self.config = config
        self.odd = int(odd)
        self.texts = cycle(config.news[self.odd:][::2])
        self.text = str(next(self.texts)) + "  |  "
        self.width, self.height = FONT4.getsize(self.text)

        # Start thread to update content this object
        self.thread = threading.Thread(target=self.update)
        self.thread.daemon = True
        self.thread.start()
        
    def setx(self, x):
        # Update text if reached left-edge
        logging.debug("!!!self.x + self.width <= 0!!!: " + str(self.x + self.width))
        self.text = str(next(self.texts)) + "  |  "
        self.sizeupdated = True
        self.x = x
        
    def draw(self, x, y, draw):
        # If content out of boundry, don't do anything
        if ( x > WIDTH or x + self.width < 0 ): return

        logging.debug(str(id(self)) + ": drawing...: " + str(self.text))
        logging.debug("x,y: " + str(x) + "," +  str(y) + " xd,yd: " + str(x + self.width) + "," + str(y + self.height) + ", width: " + str(self.width))

        # If content inside the matrix, delete the old one and draw
        draw.text( (x, y), self.text, font=FONT4, fill=RED )

    def update(self):
        while True:
            if config.news is not self.config.news:
                self.texts = cycle(config.news[self.odd:][::2])
            time.sleep(300)
        
    
class TimeContent(Content):
    def __init__(self, location=None):
        Content.__init__(self)
        if not location:
            self.timezone = datetime.now( timezone.utc ) \
                                .astimezone().tzinfo
        elif location is "Japan":
            self.timezone = pytz.timezone('Asia/Tokyo')
        elif location is "France":
            self.timezone = pytz.timezone('Europe/Paris')

        # Start thread to update time each second
        self.thread = threading.Thread(target=self.update)
        self.thread.daemon = True
        self.time = ""; self.width = 0; self.height = 0
        self.thread.start()
    
    def update(self):
        while True:
            self.time = datetime.now(self.timezone).strftime("%H:%M:%S %Z  |  ")
            self.width, self.height = FONT4.getsize(self.time) # May need to change the font
            time.sleep(.5)
        
    def draw(self, x, y, draw):
        # If content out of boundry, don't do anything
        if ( x > WIDTH or x + self.width < 0 ): return
        #logging.debug("drawing...: " + self.time)
        #logging.debug("x,y: " + str(x) + "," +  str(y) + " xd,yd: " + str(x + self.width) + "," + str(y + self.height) + ", width: " + str(self.width))
        draw.text( (x, y), self.time, font=FONT4, fill=GREY )
        

class WeatherContent(Content):
    def __init__(self, config, location=None):
        Content.__init__(self)
        # variable
        self.config = config
        self.weather = dict(config.weather)
        self.icon = Image.open("weather/0.png", 'r')
        self.sizechangeable = True; self.sizeupdated = False
        self.xspace = 1; self.yspace = 1

        # Start thread to update content this object
        self.thread = threading.Thread(target=self.update)
        self.thread.daemon = True
        self.low = (0,0); self.high = (0,0)
        self.thread.start()
        time.sleep(1)

        # Calculate size
        self.calcsize()

    def calcsize(self):
        self.width = self.icon.size[0]
        self.height = self.icon.size[1]
        
        self.tempehigh = [
            (str(self.high[1]),FONT7, DARKRED),
            ("C",FONT3, GREY),
            ("/",FONT7, WHITE),
            (str(self.high[0]),FONT3, DARKRED),
            ("F",FONT3, GREY)
        ]
        self.tempelow = [
            (str(self.low[1]),FONT7, DARKBLUE),
            ("C",FONT3, GREY),
            ("/",FONT7, WHITE),
            (str(self.low[0]),FONT3, DARKBLUE),
            ("F",FONT3, GREY)
        ]
        maxhighx = sum([ info[1].getsize(info[0])[0] for info in self.tempehigh ])
        maxhighx += self.xspace * len(self.tempehigh) 
        maxhighy = max([ info[1].getsize(info[0]) for info in self.tempehigh ], key=lambda x:x[1])[1]
        self.highsize = (maxhighx, maxhighy)

        maxlowx = sum([ info[1].getsize(info[0])[0] for info in self.tempelow ])
        maxlowx += self.xspace * len(self.tempelow)
        maxlowy = max([ info[1].getsize(info[0]) for info in self.tempelow ], key=lambda x:x[1])[1]
        self.lowsize = (maxlowx, maxlowy)
        
        self.width += max(maxhighx, maxlowx) + self.xspace
        self.height = max(self.height, maxhighy + maxlowy)
        
        
    def update(self, feel=False):
        while True:
            if self.weather is not config.weather:
                # If no data is given?
                if config.weather is {}:
                    headline = phrase =  "N/A"
                    icon = "weather/0.png"
                    max = min = (0, 0)
                else:
                    # Get headline
                    headline = config.weather["headline"]
                    # Check if it's day/night
                    t = time.time()
                    day = True if t >= config.weather["rise"] \
                          and t <= config.weather["set"] else False
                    # Select phrase & correct icon
                    phrase = config.weather["dphrase"] if day else config.weather["nphrase"]
                    iconnum = config.weather["dicon"] if day else config.weather["nicon"]
                    icon = "weather/" + str(iconnum) + ".png"
                    if not os.path.isfile(icon): icon = "weather/0.png"
                    # Get temperature info
                    min = config.weather["min"] if not feel else config.weather["rfmin"]
                    max = config.weather["max"] if not feel else config.weather["rfmax"]

                # Open icon file
                self.headline = headline
                self.phrase = phrase
                self.icon = Image.open(icon, 'r')
                self.high = max; self.low = min
                # Update height, width
                #self.height = FONT4.getsize(self.time)
                #draw.text( (x, y), self.text, font=FONT24, fill=GREY )

                # Update config
                self.config = config.weather
                self.calcsize()
                self.sizeupdated = True
            time.sleep(300)

    def draw(self, x, y, draw):
        #logging.debug("drawing weather...")
        #logging.debug("x,y: " + str(x) + "," +  str(y) + " xd,yd: " + str(x + self.width) + "," + str(y + self.height) + ", width: " + str(self.width))
        xspace = self.xspace; yspace = self.xspace
        def printing(x,y,input,pfont, pcolor):
            #logging.debug(input + " will be printed at: " + str((x,y)))
            pass
            
        def printRight(x,y,input,pfont, pcolor):
            draw.text((x,y), str(input), font=pfont, fill=pcolor)
            #printing(x,y,input,pfont, pcolor)
            return pfont.getsize(input)[0] + xspace
        
        # Icon
        widthicon = self.icon.size[0]; heighticon = self.icon.size[1]
        config.image.paste(self.icon, (x, y))
        #logging.debug("height:" + str(heighticon))

        # Max
        xoffset = x + widthicon + xspace
        for each in self.tempehigh:
            temp = printRight(xoffset, y, each[0], each[1], each[2])
            xoffset += temp

        # Min
        xoffset = x + widthicon
        yoffset = y + self.highsize[1] + yspace
        for each in self.tempelow:
            temp = printRight(xoffset, yoffset, each[0], each[1], each[2])
            xoffset += temp
 

