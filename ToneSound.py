#!/usr/bin/python3
# -*- coding: utf-8 -*-
import atexit
import pygame
import time
import sys, os
import gpiozero as gpio
import _thread as thread
from array import array
from pygame.locals import *
from morse_lookup import *
from ToneSound import *
#from twitter_news import *
from rgbmatrix import RGBMatrix#, RGBMatrixOptions

################################################################
MINKEYLENGTH = .1# .07 # Minimum dit
KEYLENGTH = .18 #dit-doh boundary
WORDLENGTH = .90 # Word boundary
DOT = "."
DASH = "-"
################################################################

import pygame
from pygame.locals import *

# Play Sound
class ToneSound(pygame.mixer.Sound):
    def __init__(self, frequency, volume):
        self.frequency = frequency
        pygame.mixer.Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        period = int(round(pygame.mixer.get_init()[0] / self.frequency))
        samples = array("h", [0] * period)
        amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
        for time in range(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples

    def play(self, input):
        if isinstance(input,str):
            self.wordToAudio(input)
        else:
            super(ToneSound, self).play(input)

    def wordToAudio(self, word):
        ditlength = (MINKEYLENGTH + KEYLENGTH ) / 2
        for char in word:
            # Print
            print(char)

            # Fullstop at space
            if char is " ":
                time.sleep( WORDLENGTH )
                continue

            # Revert char to code
            try:
                morse = list(morse_code_lookup.keys())\
                        [list(morse_code_lookup.values()).index(char.upper())]
            except:
                continue

            # Play in audio
            for ditdoh in morse:
                print (ditdoh, end="")
                self.play(-1)
                time.sleep( ditlength if ditdoh is DOT \
                            else ditlength * 3 )
                self.stop()
                time.sleep( ditlength )
            time.sleep( WORDLENGTH )
            print()
