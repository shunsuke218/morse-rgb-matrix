#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import sys, os
import gpiozero as gpio
import _thread as thread
#from array import array
from morse_lookup import *
from ToneSound import *

#from twitter_news import *
from rgbmatrix import RGBMatrix#, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont, ImageChops


import logging
import random
import threading, time

# Local class
from config import config

import pygame
from pygame.locals import *

class input_thread(threading.Thread):
    # Constructor
    def __init__(self, output):
        threading.Thread.__init__(self, args=(output,))
        self.name = "input thread"
        #self.lock = threading.Lock()
        self.config = output
        self.daemon = True

        ### Get information from config ###
        # morse
        self.MINKEYLENGTH = config.MINKEYLENGTH
        self.KEYLENGTH = config.KEYLENGTH
        self.WORDLENGTH = config.WORDLENGTH
        self.SLEEPLENGTH = config.SLEEPLENGTH
        self.DOT = config.DOT
        self.DASH = config.DASH
        # key
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
        self.XOffset = 2
        self.YOffset = 12
        self.key_up_time = time.time()
        
        # Start pygame
        #pygame.mixer.pre_init(44100, -16, 1, 1024)
        #print("init pygame")
        #pygame.init()
        #print("end init pygame")
        self.tone_obj = ToneSound(frequency = 500, volume = .5)

        # Setup key
        self.key = config.key

        self.thread_key = {
            "NEWS": "news_thread",
            "BUS": "bus_thread",
            "OUT": "output_thread",
            "EXIT": "exit"
        }


    
    def decoder_thread(self):
        new_word = False
        while True:
            time.sleep(.01)
            key_up_length = time.time() - self.key_up_time
            if key_up_length >= WORDLENGTH * 3: # End of a word
                del self.word[:]
                del self.code[:]
            if len(self.buffer) > 0 and key_up_length >= WORDLENGTH: # End of a char
                logging.debug("Deleting buffer...")
                new_word = True
                bit_string = "".join(self.buffer)
                del self.buffer[:]
            elif new_word and key_up_length >= KEYLENGTH: # Analyze key
                logging.debug("Analyzing key and add to word...")
                new_word = False
                decoded = try_decode(bit_string)
                if decoded is not None:
                    self.word.append(decoded)
                    self.code.append(bit_string)

    def run(self):
        #MatrixPrintStr("HR HR BT")
        thread.start_new_thread(self.decoder_thread, ())        
        print ("Ready")
        
        while True:
            #if "NEWS" in ''.join(config.word) : break # Change config
            logging.debug("word: " + str(config.word))
            logging.debug("buffer: " + str(config.buffer))
            # Beginning of release time
            self.key_up_time = time.time()
            # Wait for key press
            self.key.wait_for_press()
            print("pressed!")
            # Key has been pressed! beginning of press time
            key_down_time = time.time()
            # Start audio
            self.tone_obj.play(-1)
            # Wait until key release
            self.key.wait_for_release()
            print("released!")
            # Key is released. calculate time
            self.key_up_time = time.time()
            # Stop audio
            self.tone_obj.stop()

            # How long key was presseed
            key_down_length = self.key_up_time - key_down_time

            # If hold button is longer than minimum length
            if key_down_length > self.SLEEPLENGTH:
                self.config.set_global_status( "sleep" )
            elif key_down_length > MINKEYLENGTH:
                if self.config.get_global_status() is "sleep":
                    self.config.set_global_status("output_thread")
                # Add DIT/DOH
                self.buffer.append(DASH if key_down_length > KEYLENGTH else DOT)

            word = "".join(config.word)
            logging.debug("word: " + str(word) )
            status = [ key for key in ("NEWS", "BUS", "EXIT", "OUT") \
                       if word is not None and key in word ]
            if any(status):
                logging.debug("status change!! " + str(status) )
                self.config.set_global_status( self.thread_key[status[0]] )

            # Print current words
            #print (config.word)
            #print (''.join(config.word) if config.word is not None else "")


            


if __name__ == '__main__':
    config = config()
    item = input_thread(config)
    item.run()
