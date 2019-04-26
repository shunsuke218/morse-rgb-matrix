#!/usr/bin/python3
# -*- coding: utf-8 -*-

from config import *

import logging

class matrix_manip():
    # Constructor
    def __init__(self):
        logging.debug("matrix_manip is init-ing")
        self.config = config
        # XOffset for print
        self.XOffset = 2
        self.YOffset = 4

    def MatrixPrintChar(self, char, bit):
        # Calculate width of char
        charWidth = FONT24.getsize(char)[0]
        # If new character exceed image width
        if ( self.XOffset + charWidth ) > WIDTH:
            # Calculate the needed width
            needed = ( self.XOffset + charWidth + 2 ) - WIDTH
            # Move the image to the left by needed
            config.image.paste(config.image, (-needed, 0) )
            # Update XOffset
            self.XOffset -= needed
            # Delete right of XOffset
            config.draw.rectangle( \
                (self.XOffset, 0, WIDTH, HEIGHT), fill= (0,0,0,0) )

        # Draw text
        config.draw.text( \
            (self.XOffset, self.YOffset), char, font=FONT24 )
        # Draw morse code
        bitWidth = FONT9.getsize(bit)[0]
        bitOffset = self.XOffset + ( (charWidth - bitWidth) / 2 )
        config.draw.text( \
            (bitOffset, self.YOffset + 16), bit, font=FONT9 )

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
            (0, 0, WIDTH, HEIGHT), fill=(0,0,0,0) ) 
