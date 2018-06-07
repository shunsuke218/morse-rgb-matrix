#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import threading, time
from time import datetime, strftime

# Local class
from weather import *
from stock import *
from twitter_news import *


# TODO: Create extended classes based on Content class
class Content:
    # Will be overrode
    def __init__(self, init):
        self.content = ""
        self.width = 0
    def draw(self, x, y, draw):
        draw.text(x, y, self.content, font=FONT24)


class TimeContent(Content):
    def __init__(self, location=None):
        if not location:
            self.timezone = datetime.datetime.now( datetime.timezone.utc )\
                                .astimezone().tzinfo
        elif location is "Japan":
            self.timezone = pytz.timezone('Asia/Tokyo')
        elif location is "France":
            self.timezone = pytz.timezone('Europe/Paris')
        self.thread = threading.Thread(target=self.update)
        self.time = ""; self.width = 0
        self.thread.run()
        time.sleep(2)
    
    def update():
        while True:
            self.time = datetime.now(self.timezone).strftime("%H:%M:%S %Z")
            self.width, self.height = FONT8.getsize(self.time)[0]
            time.sleep(.8)

    def draw(self, XOffset, YOffset, draw):
        draw.text( \
            (XOffset, YOffset), self.time, font=FONT8 )
        
