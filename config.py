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
INFOLENGTH = 60 # Goto Info Threadx
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
FONT4 = ImageFont.truetype("pixel.ttf", 5)
FONT8 = ImageFont.load( \
    os.path.dirname(os.path.realpath(__file__) ) \
    + '/helvR08.pil')
################################################################
# Color Setting
GREEN = ( 0, 255, 0)
DARKGREEN = ( 110, 255, 110)
YELLOW = (255, 255, 0)
DARKYELLOW = (255, 255, 110)
RED = (255, 0, 0)
DARKRED = (255, 110, 110)
BLUE = ( 0, 0, 255)
DARKBLUE = ( 110, 110, 255)
GREY = (110, 110, 110)
WHITE = (0, 0, 0)
################################################################
# News Setting
NEWS_INTERVAL = 300
# Weather Setting
WEATHER_INTERVAL = 1800
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
    # Weather
    weather = {}

    # Constructor
    def __init__(self):
        #self.global_status = ["output_thread"]
        self.global_status = ["info_thread"]
        #self.matrix_manip = MatrixManip(self)


    # Setter
    def set_global_status(self, status):
        self.global_status = [status]

    # Getter
    def get_global_status(self):
        return self.global_status[0]

    
