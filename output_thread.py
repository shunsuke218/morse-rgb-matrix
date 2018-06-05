#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import threading, time

# Local class
from config import config
from morse_lookup import *

class output_thread(threading.Thread):
    # Constructor
    def __init__(self, output):
        # Thread settings
        threading.Thread.__init__(self, args=(output,))
        self.name = "output thread"
        self.daemon = True
        self.lock = threading.Lock()
        # Config
        self.config = output
        # XOffset for print
        self.XOffset = 2
        self.YOffset = 4

    def MatrixPrintChar(self, char, bit):
        # Calculate width of char
        charWidth = config.FONT24.getsize(char)[0]
        # If new character exceed image width
        if ( self.XOffset + charWidth ) > config.WIDTH:
            # Calculate the needed width
            needed = ( self.XOffset + charWidth + 2 ) - config.WIDTH
            # Move the image to the left by needed
            config.image.paste(config.image, (-needed, 0) )
            # Update XOffset
            self.XOffset -= needed
            # Delete right of XOffset
            config.draw.rectangle( \
                (self.XOffset, 0, config.WIDTH, config.HEIGHT), fill= (0,0,0,0) )

        # Draw text
        config.draw.text( \
            (self.XOffset, self.YOffset), char, font=config.FONT24 )
        # Draw morse code
        bitWidth = config.FONT9.getsize(bit)[0]
        bitOffset = self.XOffset + ( (charWidth - bitWidth) / 2 )
        config.draw.text( \
            (bitOffset, self.YOffset + 14), bit, font=config.FONT9 )
        
        logging.debug ("input: " + str(char) )
        logging.debug ("bit: " + str(bit) )
        logging.debug ("charWidth: " + str(charWidth) )
        logging.debug ("XOffset: " + str(self.XOffset) )

        # Clear Matrix
        config.matrix.Clear()
        # Show Image to the Matrix
        config.matrix.SetImage(config.image, 0, 0)
        # Update offset
        self.XOffset += charWidth 

    '''
    def MatrixPrintStr(self, input):
        for char in input:
            bit = to_keys(char)
            if bit is not None:
                print ("printing: ", char, bit)
                self.MatrixPrintChar(char, bit)
            config.tone_obj.play(char)
    '''
    
    def MatrixPrintDelete(self):
        # Set XOffset to default
        self.XOffset = 2 
        # Clear Matrix
        config.matrix.Clear() 
        # Reset Image
        config.draw.rectangle( \
            (0, 0, config.WIDTH, config.HEIGHT), fill=(0,0,0,0) ) 


    # Main section
    def run(self):
        #MatrixPrintStr("HR HR BT")
        while True:
            # Check the state, wait if others are in progress
            self.lock.acquire()
            # Clean Matrix
            self.MatrixPrintDelete()
            local_word = config.word[:]
            no_action = time.time()

            # Do Stuff
            while True:
                # Check if state has changed
                if self.config.get_global_status() is not "output_thread": break
                # Check if no input for 60 seconds
                if no_action - time.time() > 30:
                    self.config.set_global_status("info_thread"); break
                    
                # Check if word has updated
                if not local_word == config.word:
                    no_action = time.time()
                    if len(local_word) < len(config.word):
                        # Word added
                        self.MatrixPrintChar(config.word[-1], config.code[-1])
                    else:
                        # Word deleted
                        self.MatrixPrintDelete()
                    # Update word
                    local_word = config.word[:]
                time.sleep(1)

            # State changed; Clean up before sleep
            self.MatrixPrintDelete()
            time.sleep(1)
