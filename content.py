#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import threading, time
from datetime import datetime, timezone
from time import strftime
import pytz

# Local class
#from weather import *
#from stock import *
from twitter_news import *



# TODO: Create extended classes based on Content class
class Content:
    # Will be overrode
    def __init__(self, init):
        self.content = ""
        self.width = 0
        self.x = 0

    def move(self):
        self.x -= 1
            
    def draw(self, x, y, draw):
        draw.text(x, y, self.content, font=FONT24)


class TimeContent(Content):
    def __init__(self, location=None):
        self.x = 0
        if not location:
            self.timezone = datetime.now( timezone.utc )\
                                .astimezone().tzinfo
        elif location is "Japan":
            self.timezone = pytz.timezone('Asia/Tokyo')
        elif location is "France":
            self.timezone = pytz.timezone('Europe/Paris')
        self.thread = threading.Thread(target=self.update)
        self.thread.daemon = True
        self.time = ""; self.width = 0
        self.thread.start()
        time.sleep(0.5)
    
    def update(self):
        while True:
            self.time = datetime.now(self.timezone).strftime("   %H:%M:%S %Z   |")
            self.width, self.height = FONT8.getsize(self.time)
            time.sleep(.5)

    def draw(self, XOffset, YOffset, draw):
        draw.rectangle( (XOffset, YOffset, self.width, self.height), \
            fill= (0,0,0,0) )
        
        draw.text( \
            (XOffset, YOffset), self.time, font=FONT8 )
        
