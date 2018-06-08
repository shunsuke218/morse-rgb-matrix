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
        # Time
        self.tiles.append( \
            Tile( [ TimeContent(n) for n in (None, "Japan", None, "France") ], config) )
        self.tiles[0].speed = 1
        # Text
        logging.debug("[0] height: " + str(self.tiles[0].height))
        self.tiles.append( \
            Tile([ HogeContent(),HogeContent() ], config, self.tiles[0].height + 1) )
        logging.debug("[1] height: " + str(self.tiles[1].height) + " YOffset: " + str(self.tiles[1].YOffset) )
        self.tiles[1].speed = 5
        # Time
        self.tiles.append( \
            Tile( [ TimeContent(n) for n in (None, "Japan", None, "France") ], config, self.tiles[1].YOffset + self.tiles[1].height) )
        self.tiles[2].speed = 4
        '''
        self.tiles.append( \
            Tile( [ WeatherContent(), StockContent(),  ], config, tiles[0].height )
        )
        self.tiles.append( \
            Tile( [ ], config, tiles[1].YOffset + tiles[1].height )
        )
        '''

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
        if ( sum( [ content.width for content in self.contents ] ) < WIDTH ):
            raise Exception ("Content in the tile is not enough to fill the Matrix!")
        # Fill up the tile with contents
        self.fill()
        self.height = max ( [ content.height for content in self.contents  ] )

    def rotate(self):
        # Rotate list
        self.contents = self.contents[1:] + self.contents[:1]

    def fill(self):
        for content in self.contents:
            content.draw(self.XOffset, self.YOffset, config.draw)
            content.x = self.XOffset
            self.XOffset = self.XOffset + content.width
        """
        while self.XOffset < WIDTH:
            content = self.contents[0] #; self.rotate()
            self.contents = self.contents[1:] + self.contents[:1]
            content.draw(self.XOffset, self.YOffset, config.draw)
            content.x = self.XOffset
            self.XOffset = self.XOffset + content.width
        """

    def update(self, content):
        # Move object to the right-end
        if content.x + content.width > 0:
            return
        content.x = self.XOffset
        self.XOffset = self.XOffset + content.width
        
    def draw(self):
        self.config = config
        # Clear whole tile area
        config.draw.rectangle( (0, self.YOffset, WIDTH, self.height), fill= (0,0,0,0) )
        
        # Move left by one
        #config.image.paste(config.image, (-1 * self.speed, self.YOffset))
        [ content.move(self.speed) for content in self.contents ]
        self.XOffset -= 1 * self.speed

        # If image is out of boundary, update x
        [ self.update(content) for content in self.contents ]

        # Draw content
        #config.draw.rectangle( (self.XOffset, self.YOffset, WIDTH, self.height), fill= (0,0,0,0) )
        [ content.draw(content.x, self.YOffset, config.draw) for content in self.contents ]
        #config.draw.rectangle( (WIDTH - 1, 0, WIDTH, HEIGHT), fill= (0,0,0,0) )

            

        
