#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rgbmatrix import RGBMatrix
from PIL import Image, ImageDraw, ImageFont
import gpiozero as gpio

from ToneSound import *
#from MatrixManip import *

################################################################
# Morse Code Setting
MINKEYLENGTH = .10 # .07 # Minimum dit
KEYLENGTH = .20 #dit-doh boundary
WORDLENGTH = .90 # Word boundary
SLEEPLENGTH = 2 # Goto Sleep
DOT = "."; DASH = "-"    
################################################################
# Key Setting
PIN = 25
################################################################
# Matrix Setting
WIDTH, HEIGHT = 64, 32
################################################################
# Image Setting
FONT24 = ImageFont.truetype("helv.ttf", 24)
FONT9 = ImageFont.truetype("helv.ttf", 9)
################################################################
# News Setting
NEWS_INTERVAL = 300
################################################################

class config():
    # Variables
    key_down_time = 0
    key_down_length = 0
    key_up_time = 0
    buffer = []; word = []; code = []

    # Tone Object
    tone_obj = ToneSound(frequency = 500, volume = .5)
    # Key Setting
    key = gpio.Button(PIN, pull_up = True)
    # Matrix Setting
    matrix = RGBMatrix(32, 2)
    #matrix_manip = MatrixManip()
    # Image Setting
    image = Image.new('RGB', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    # News
    news = None

    # Constructor
    def __init__(self):
        #self.global_status = ["output_thread"]
        self.global_status = ["news_thread"]
        #self.matrix_manip = MatrixManip(self)


    # Setter
    def set_global_status(self, status):
        self.global_status = [status]

    # Getter
    def get_global_status(self):
        return self.global_status[0]

    
