#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import random
import threading, time

# Local class
from config import config
from morse_lookup import *

class output_thread(threading.Thread):
    # Constructor
    def __init__(self, output):
        threading.Thread.__init__(self, args=(output,))
        self.name = "output thread"
        self.lock = threading.Lock()
        self.config = output
        self.daemon = True
        self.XOffset = 2

    def MatrixPrintChar(self, char, bit):
        charWidth = config.FONT24.getsize(char)[0]
        if ( self.XOffset + charWidth ) > config.WIDTH:
            needed = ( self.XOffset + charWidth + 2 ) - config.WIDTH 
            config.image.paste(config.image, (-needed, 0) )
            self.XOffset -= needed
            config.draw.rectangle( (self.XOffset, 0, config.WIDTH, config.HEIGHT), fill= (0,0,0,0) )

        # Draw text
        config.draw.text( (self.XOffset, 2), char, font=config.FONT24)
        # Draw code
        bitWidth = config.FONT9.getsize(bit)[0]
        bitOffset = self.XOffset + ( (charWidth - bitWidth) / 2 )
        config.draw.text( (bitOffset, 18), bit, font=config.FONT9)
        
        print ("input: ", char)
        print ("bit: ", bit)
        print ("charWidth: ", charWidth)
        print ("XOffset: ", self.XOffset)

        config.matrix.Clear() # Clear Matrix
        config.matrix.SetImage(config.image, 0, 0)
        # Update offset
        self.XOffset += charWidth 

    def MatrixPrintStr(self, input):
        for char in input:
            bit = to_keys(char)
            if bit is not None:
                print ("printing: ", char, bit)
                self.MatrixPrintChar(char, bit)
            #tone_obj.play(char)

    def MatrixPrintDelete(self):
        self.XOffset = 2 # Set XOffset to 0
        config.matrix.Clear() # Clear Matrix
        config.draw.rectangle( (0, 0, config.WIDTH, config.HEIGHT), fill=(0,0,0,0)) # Reset Image


    # Main section
    def run(self):
        while True:
            # Check the state, wait if others are in progress
            self.lock.acquire()

            # Do Stuff
            #local_word = list(config.word)
            local_word = config.word[:]
            while True:
                logging.debug("global: " + str(self.config.get_global_status()))
                logging.debug("local_word: " + str(local_word) )
                logging.debug("config.word: " + str(config.word) )
                if not local_word == config.word:
                    logging.debug("len(local_word): " + str(len(local_word)))
                    logging.debug("len(config.word): " + str(len(config.word)))
                    if len(local_word) < len(config.word): # Added word
                        logging.debug("word added!!")
                        self.MatrixPrintChar(config.word[-1], config.code[-1])
                        #self.MatrixPrintStr(config.word[-1])
                        ### TODO ###
                        # Why need to re-convert char to code?
                        # Don't we already have the code by user?
                        # We should preserve the direct input and
                        # Recycle it over here.
                        # self.MatrixPrintStr(config.word[-1], config.code[-1])
                    else: # Word deleted
                        logging.debug("word deleted!!!")
                        self.MatrixPrintDelete()
                local_word = config.word[:]
                
                time.sleep(1)
                """
                num = random.randint(1,1000)
                logging.debug("num: " + str(num) + \
                              ", change? " + str((num > 500)) )
                time.sleep(.1)

                # If signal sent, change state
                if (num > 750):
                    break

            #Exitting state; change config to the next state
            decision = "info_thread" if random.randint(0,1) else "news_thread"
            logging.debug("global_status has been updated!!" + str(self.config.get_global_status()) + "->" +  decision)
                """
            self.config.set_global_status(decision)
            time.sleep(3)
