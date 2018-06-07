#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import threading, time

# Local class
from config import *
from content import *

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

        # Time information
        self.tiles = []
        self.tiles.append( \
            Tile( [ TimeContent(n) for n in (None, "Japan", "France") ], config) )
        '''
        self.tiles.append( \
            Tile( [ WeatherContent(), StockContent(),  ], config,  )
        )

        # Weather Thread
        self.weather = threading.Thread(target=getWeather)
        self.weather.daemon = True
        self.weather.name = "Weather"
        # Stock Thread
        self.stock = threading.Thread(target=getStock)
        self.stock.daemon = True
        self.stock.name = "Stock"
        '''
        # Twitter News Thread
        self.twitter = threading.Thread(target=getNews)
        self.twitter.daemon = True
        self.twitter.name = "Twitter News"

    # Main section
    def run(self):
        #self.weather.start() # Merge this with "Twitter News" in News?
        #self.stock.start()
        #self.twitter.start()
        while True:
            # Check the state, wait if others are in progress
            self.lock.acquire()
            logging.debug("info_thread is released...")
            # Clear Matrix
            self.config.matrix.Clear()
            # Do Stuff
            while True:
                # Check if state has changed
                if self.config.get_global_status() is not "info_thread": break
                # DO STUFF
                for tile in self.tiles:
                    tile.draw()
                    #tile.XOffset -= 1 * tile.speed
                self.config.matrix.Clear()
                self.config.matrix.SetImage(config.image, 0, 0)
                time.sleep(.1)
            # State changed; Clean up before change state
            self.config.matrix.Clear()
            #self.global_status.set_global_status("output_thread")
            time.sleep(1)




class Tile():
    def __init__(self, contents, config, YOffset = 0):
        self.XOffset = 0; self.YOffset = YOffset
        self.tileWidth = 0
        self.speed = 1
        self.contents = contents # list object
        self.config = config
        # Fill up the tile with contents
        self.height = max ( [ content.height for content in self.contents  ] )
        self.fill()

    def rotate(self):
        # Rotate list
        self.contents = self.contents[1:] + self.contents[:1]

    def fill(self):
        while self.XOffset < WIDTH:
            self.add()
            
    def add(self):
        self.content = self.contents[0]
        self.rotate()
        self.content.draw(self.XOffset, self.YOffset, config.draw)
        self.content.x = self.XOffset
        self.XOffset = self.XOffset + self.content.width

    def draw(self):
        self.config = config
        # Move left by one
        config.image.paste(config.image, (-1, self.YOffset))
        [ content.move() for content in self.contents ]
        self.XOffset -= 1
        if ( self.XOffset ) <= WIDTH:
            # Right edge reached Matrix Edge
            logging.debug("Right edge reached Matrix Edge")
            self.add()
        
        [ content.draw(content.x, self.YOffset, config.draw) for content in self.contents ]
            

        
