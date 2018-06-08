#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import threading, time
from datetime import datetime, timezone
from time import strftime
import pytz

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

    def move(self, num=1):
        self.x -= num
            
    def draw(self, x, y, draw):
        return

class HogeContent(Content):
    def __init__(self):
        Content.__init__(self)
        self.text = "hoge"
        self.width, self.height = FONT24.getsize(self.text)

        
    def draw(self, x, y, draw):
        logging.debug("drawing...: " + self.text)
        logging.debug("x,y: " + str(x) + "," +  str(y) + " xd,yd: " + str(x + self.width) + "," + str(y + self.height))
        # If content out of boundry, don't do anything
        if ( x > WIDTH or x + self.width < 0 ): return
        # If content inside the matrix, delete the old one and draw
        draw.rectangle( (x, y, self.width, y + self.height), \
            fill= (0,0,0,0) )
        draw.text( (x, y), self.text, font=FONT24, fill=(110, 110, 110) )
    
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
            self.time = datetime.now(self.timezone).strftime("%H:%M:%S %Z   ")
            self.width, self.height = FONT4.getsize(self.time) # May need to change the font
            time.sleep(.5)

        
    def draw(self, x, y, draw):
        # If content out of boundry, don't do anything
        if ( x > WIDTH or x + self.width < 0 ): return

        logging.debug("drawing...: " + self.time)
        logging.debug("x,y: " + str(x) + "," +  str(y) + " xd,yd: " + str(x + self.width) + "," + str(y + self.height))

        # If content inside the matrix, delete the old one and draw
        # MAY NOT NEEDED ANYMORE
        draw.rectangle( (x, y, self.width, y + self.height), \
            fill= (0,0,0,0) )
        draw.text( (x, y), self.time, font=FONT4, fill=(110, 110, 110) )
        

class WeatherContent(Content):
    def __init__(self, config, location=None):
        Content.__init__(self)
        # variable
        self.config = config
        self.weather = dict(config.weather)
        # Start thread to update content this object
        self.thread = threading.Thread(target=self.update)
        self.thread.daemon = True
        self.thread.start()

    def update(self, feel=False):
        while True:
            if cmp(self.config, config.weather):
                # If no data is given?
                if config.weather is {}:
                    headline = "N/A"
                    phrase = "N/A"
                    icon = "weather/0.png"
                    max = (0, 0)
                    min = (0, 0)
                else:
                    # Get headline
                    headline = config.weather["headline"]
                    # Check if it's day/night
                    t = time.time()
                    day = True \
                          if t >= config.weather["rise"] and t <= config.weather["set"] \
                             else False
                    # Select phrase & correct icon
                    phrase = config.weather["dphrase"] if day else config.weather["nphrase"]
                    iconnum = config.weather["dicon"] if day else config.weather["nicon"]
                    icon = "weather/" + str(iconnum) + ".png" if os.path.isfile(icon) \
                           else "weather/0.png"
                    # Get temperature info
                    min = config.weather["min"] if not feel \
                          else config.weather["rfmin"]
                    max = config.weather["max"] if not feel \
                          else config.weather["rfmax"]
                    
                # Open icon file
                self.headline = headline
                self.phrase = phrase
                self.icon = Image.open(icon, 'r')
                self.max = max
                self.min = min
                # Update height, width
                #self.height = FONT4.getsize(self.time)
                #draw.text( (x, y), self.text, font=FONT24, fill=GREY )
                
                # Update config
                self.config = config.weather
            time.sleep(300)

    def draw(self, x, y):
        xoffset = x; yoffset = y
        xspace = 2; yspace = 2
        # Icon
        config.image.paste(self.icon, (x, y))
        widthicon = self.icon[0]
        heighticon = self.icon[1]

        xoffset += widthicon + xspace

        # Max temp
        # 13: c 
        draw.text( (xoffset, y), self.max[0], font=FONT24, fill=RED )
        widthc, widthy = FONT24.getsize( str(self.max[0]) )
        xoffset += widthc + xspace
        yoffset += heightc + yspace
        # C: unit
        draw.text( (xoffset, yoffset), "C", font=FONT9, fill=WHITE )
        widthc, widthy = FONT9.getsize( "C" )
        xoffset += widthc + xspace
        yoffset += heightc + yspace
        # 57F: f
        draw.text( (xoffset, yoffset), self.max[1], font=FONT9, fill=DARKRED )
        widthc, widthy = FONT9.getsize( str(self.max[1]) )
        xoffset += widthc + xspace
        yoffset += heightc + yspace


        xoffset = widthicon;
        # Min temp
        # 26: c 
        draw.text( (xoffset, y), self.min[0], font=FONT24, fill=BLUE )
        widthc, widthy = FONT24.getsize( str(self.max[0]) )
        xoffset += widthc + xspace
        yoffset += heightc + yspace
        # C: unit
        draw.text( (xoffset, yoffset), "C", font=FONT9, fill=WHITE )
        widthc, widthy = FONT9.getsize( "C" )
        xoffset += widthc + xspace
        yoffset += heightc + yspace
        # 79F: f
        draw.text( (xoffset, yoffset), self.min[1], font=FONT9, fill=DARKBLUE )
        widthc, widthy = FONT9.getsize( str(self.max[1]) )
        xoffset += widthc + xspace
        yoffset += heightc + yspace
        
