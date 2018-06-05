#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import threading, time

# Local class
from config import *
from MatrixManip import *
from twitter_news import *
from weather import *
from stock import *

class info_thread(threading.Thread):
    # Constructor
    def __init__(self, input):
        threading.Thread.__init__(self, args=(input,))
        self.name = "info thread"
        self.lock = threading.Lock()
        self.global_status = input
        self.daemon = True
        # Config
        self.config = input
        self.matrix_manip = MatrixManip(self.config)
        # Weather Thread
        self.weather = threading.Thread(target=getWeather)
        self.weather.daemon = True
        self.weather.name = "Weather"
        # Stock Thread
        self.stock = threading.Thread(target=getStock)
        self.stock.daemon = True
        self.stock.name = "Stock"

    # Main section
    def run(self):
        self.weather.start() # Merge this with "Twitter News" in News?
        self.stock.start()
        while True:
            # Check the state, wait if others are in progress
            self.lock.acquire()
            # Clean Matrix
            self.matrix_manip.MatrixPrintDelete()

            # Do Stuff
            while True:
                # Check if state has changed
                if self.config.get_global_status() is not "info_thread": break
                # DO STUFF
                for tile in tiles:
                    if tile.XOffset < WIDTH:
                        tile.draw()
                        tile.XOffset -= 1 * tile.speed
                        tile.tileWidth -= 1 * tile.speed


            # State changed; Clean up before sleep
            self.matrix_manip.MatrixPrintDelete()
            #self.global_status.set_global_status("output_thread")
            time.sleep(1)




class Tile():
    def __init__(self, YOffset, contents, config):
        self.XOffset = 0; self.YOffset = 0
        self.tileWidth = 0
        self.speed = 1
        self.contents = contents # list object
        self.config = config
        # Fill up the tile with contents
        x = 0
        while x < WIDTH: x = self.draw()
            
    def draw():
        content = self.contents[0]
        # Rotate list
        self.contents = self.contents[1:] + self.contents[:1]
        width = content.width()
        if ( self.XOffset + width ) > WIDTH:
            needed = ( self.XOffset + x + 2 ) - WIDTH
            self.config.image.paste(config.image, (-needed, self.YOffset) )
            self.XOffset -= needed
            self.config.draw.rectangle( \
                (self.XOffset, self.YOffset, WIDTH, HEIGHT), fill= (0,0,0,0) )
        content.draw(self.XOffset, self.YOffset, config.draw)
        self.XOffset += width
        return width

    # TODO: Create extended classes based on Content class
    class Content:
        # Will be overrided
        def __init__(self, init):
            self.content = "hoge"
            self.width = FONT24.getsize(self.content)[0]
        def draw(self, x, y, draw):
            draw.text(x, y, self.content, font=FONT24)
        
        
        
