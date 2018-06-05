#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os, sys
import threading, time
import gpiozero as gpio
import _thread as thread

# Local class
from config import config

from PIL import Image, ImageDraw, ImageFont, ImageChops
from ToneSound import *
#from twitter_news import *
from morse_lookup import *
from rgbmatrix import RGBMatrix

# - * - * - * -
# Could be deleted?
import pygame
from pygame.locals import *
# - * - * - * -

class input_thread(threading.Thread):
    # Constructor
    def __init__(self, output):
        threading.Thread.__init__(self, args=(output,))
        self.name = "input thread"
        self.daemon = True
        # Config
        self.config = output

        ### Get information from config ###
        # morse
        self.MINKEYLENGTH = config.MINKEYLENGTH
        self.KEYLENGTH = config.KEYLENGTH
        self.WORDLENGTH = config.WORDLENGTH
        self.SLEEPLENGTH = config.SLEEPLENGTH
        self.DOT, self.DASH = config.DOT, config.DASH, 
        # key
        self.key = config.key
        self.pin = config.PIN
        # matrix
        self.matrix = config.matrix
        self.width, self.height = config.WIDTH, config.HEIGHT
        # image & draw
        self.font24 = config.FONT24
        self.font9 = config.FONT9
        self.image = config.image
        self.draw = config.draw
        # Word & buffer
        self.word = config.word
        self.code = config.code
        self.buffer = config.buffer
        ###################################

        # Local variable
        self.key_up_time = time.time()
        
        # Start pygame
        self.tone_obj = ToneSound(frequency = 500, volume = .5) # Maybe in config instead?

        # Setup key
        self.thread_key = {
            "INFO": "info_thread",
            "NEWS": "news_thread",
            "BUS": "bus_thread",
            "OUT": "output_thread",
            "SLEEP": "sleep",
            "EXIT": "exit"
        }

    def decoder_thread(self):
        new_word = False
        while True:
            # How long key was released
            key_up_length = time.time() - self.key_up_time

            # If key was released longer than the threshold...
            if key_up_length >= WORDLENGTH * 3:
                # Longest: end of a word; delete word/buffer
                del self.word[:]; del self.code[:]
            elif len(self.buffer) > 0 \
               and key_up_length >= WORDLENGTH:
                # Mid-Long: end of a char; delete buffer
                new_word = True
                bit_string = "".join(self.buffer)
                del self.buffer[:]
            elif new_word and key_up_length >= KEYLENGTH:
                # Minimum: end of a DIT/DOH; analyze key
                new_word = False
                decoded = try_decode(bit_string)
                if decoded:
                    # If can be decoded, add to word/code list
                    self.word.append(decoded)
                    self.code.append(bit_string)
            else:
                # Other: noise or in the middle of input
                pass
            time.sleep(.01)

            
    def run(self):
        # Start Thread
        thread.start_new_thread(self.decoder_thread, ())

        while True:
            # Print current word/buffer
            logging.debug("word: " + str(config.word))
            logging.debug("buffer: " + str(config.buffer))

            # Waiting for key to be pressed
            self.key_up_time = time.time()
            self.key.wait_for_press()

            # Instance of key pressed
            logging.debug("pressed!")
            key_down_time = time.time()
            self.tone_obj.play(-1)

            # Wait for key to be released
            self.key.wait_for_release()

            # Instance of key released
            logging.debug("released!")
            self.key_up_time = time.time()
            self.tone_obj.stop()
            
            # How long key was presseed
            key_down_length = self.key_up_time - key_down_time
            
            # If key was pressed loger than the threshold...
            if key_down_length > SLEEPLENGTH:
                # Longest: go to sleep state
                self.config.set_global_status( "sleep" )
            elif key_down_length > MINKEYLENGTH:
                # Minimum: DIT/DOH input
                if self.config.get_global_status() is not "output_thread":
                    # Exit non-output state to output state
                    self.config.set_global_status("output_thread")
                # Add DIT/DOH to buffer
                self.buffer.append(DASH if key_down_length > KEYLENGTH else DOT)

            # Check if word input matches a keyword
            word = "".join(config.word)
            logging.debug("word: " + str(word) )
            status = [ key for key in self.thread_key.keys() \
                       if word is not None and key in word ]
            if any(status):
                # Change state
                logging.debug("status change!! " + str(status) )
                self.config.set_global_status( self.thread_key[status[0]] )
