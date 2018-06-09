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
        # Thread information
        threading.Thread.__init__(self, args=(input,))
        self.name = "info thread"
        self.lock = threading.Lock()
        self.global_status = input
        self.daemon = True


        # Config
        self.config = input

        # Tiles
        self.tiles = []
        YOffset = 0
        # Time
        self.tiles.append( \
            Tile( [ TimeContent(n) for n in (None, "Japan", None, "France") ], config) )
        self.tiles[0].speed = 2
        YOffset += self.tiles[0].height + 2
        logging.debug("[0] height: " + str(self.tiles[0].height) + " YOffset: " + str(YOffset))

        # Weather
        self.tiles.append( \
            Tile( [ WeatherContent(config), HogeContent(), WeatherContent(config), HogeContent() ], config, YOffset) )
        self.tiles[1].speed = 3
        YOffset += self.tiles[1].height + 2
        logging.debug("[1] height: " + str(self.tiles[1].height) + " YOffset: " + str(YOffset))

        # News
        self.tiles.append( \
            Tile( [ NewsContent(config), NewsContent(config, True) ], config, YOffset) )
        self.tiles[2].speed = 4
        YOffset += self.tiles[2].height + 2
        logging.debug("[2] height: " + str(self.tiles[2].height) + " YOffset: " + str(YOffset))
        """
        self.tiles.append( \
            Tile( [ TimeContent(n) for n in ("Japan", "France", "Japan", None, "Japan", "France") ], config, YOffset) )
        self.tiles[2].speed = 5
        YOffset += self.tiles[2].height + 2
        logging.debug("[2] height: " + str(self.tiles[2].height) + " YOffset: " + str(YOffset))

        self.tiles.append( \
            Tile( [ WeatherContent(config), HogeContent(), HogeContent() ], config, YOffset) )
        self.tiles[3].speed = 4
        YOffset += self.tiles[3].height + 2
        """


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
                self.config.matrix.Clear()
                self.config.matrix.SetImage(config.image, 0, 0)
                time.sleep(.15)

            # State changed; Clean up before change state
            self.config.matrix.Clear()
            #self.global_status.set_global_status("output_thread")
            time.sleep(1)




class Tile():
    def __init__(self, contents, config, YOffset = 0):
        self.XOffset = 0; self.YOffset = YOffset
        self.speed = 1 # Speed 
        self.contents = contents # list object
        self.config = config
        self.sizechangeable = any( [ content.sizechangeable for content in self.contents] )
        """
        if ( sum( [ content.width for content in self.contents ] ) < WIDTH ):
            raise Exception ("Content in the tile is not enough to fill the Matrix!")
        """
        # Fill up the tile with contents
        self.fill()
        self.height = max ( [ content.height for content in self.contents  ] )
        logging.debug("This tile's offset: " + str(self.XOffset) + "," + str(self.YOffset))

    def fill(self):
        for content in self.contents:
            logging.debug("Going to draw: " + str(self.XOffset) + "," + str(self.YOffset))
            content.draw(self.XOffset, self.YOffset, config.draw)
            content.x = self.XOffset
            self.XOffset = self.XOffset + content.width

    def changesize(self):
        # Find the index of left-most object
        minindex = min( \
                enumerate( [ content.x for content in self.contents ] ), \
                key=lambda x:x[1]) [0]
        logging.debug([ content.x for content in self.contents ])
        logging.debug(minindex)
        self.XOffset = self.contents[minindex].x
        for content in self.contents[minindex:] + self.contents[:minindex]:
            content.x = self.XOffset
            self.XOffset += content.width
            content.sizeupdated = False
        #self.XOffset = sum([ content.width for content in self.contents ])
        
    def update(self, content):
        # Move object to the right-end
        # return if content is at right of the left-boundary
        if content.x + content.width > 0: return
        content.setx(self.XOffset)
        self.XOffset = self.XOffset + content.width
        
    def draw(self):
        self.config = config
        
        # Clear whole tile area
        config.draw.rectangle( (0, self.YOffset, WIDTH, self.YOffset + self.height), fill= (0,0,0,0) )

        # Update x if any content is size-changeable
        if self.sizechangeable and any([content.sizeupdated for content in self.contents]):
            self.changesize()
            

        # Move left by one
        [ content.move(self.speed) for content in self.contents ]
        self.XOffset -= 1 * self.speed

        # If image is out of boundary, update x
        [ self.update(content) for content in self.contents ]

        # Draw
        [ content.draw(content.x, self.YOffset, config.draw) for content in self.contents ]

            

        
