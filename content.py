#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import threading, time
from datetime import datetime, timezone
from time import strftime
import pytz

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
        time.sleep(0.5)
    
    def update(self):
        while True:
            self.time = datetime.now(self.timezone).strftime("%H:%M:%S %Z   ")
            self.width, self.height = FONT4.getsize(self.time) # May need to change the font
            time.sleep(.5)

    def draw(self, x, y, draw):
        # If content out of boundry, don't do anything
        logging.debug("drawing...: " + self.time)
        logging.debug("x,y: " + str(x) + "," +  str(y) + " xd,yd: " + str(x + self.width) + "," + str(y + self.height))
        if ( x > WIDTH or x + self.width < 0 ): return
        # If content inside the matrix, delete the old one and draw
        draw.rectangle( (x, y, self.width, y + self.height), \
            fill= (0,0,0,0) )
        draw.text( (x, y), self.time, font=FONT4, fill=(110, 110, 110) )
        
