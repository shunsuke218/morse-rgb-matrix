#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont
import gpiozero as gpio

from ToneSound import *
#from MatrixManip import *

################################################################
# Morse Code Setting
MINKEYLENGTH = .10 # .07 # Minimum dit
KEYLENGTH = .20 #dit-doh boundary
WORDLENGTH = 1.60 # Word boundary
SLEEPLENGTH = 2 # Goto Sleep
INFOLENGTH = 60 # Goto Info Thread
DOT = "."; DASH = "-"    
################################################################
# Key Setting
PIN = 25 # (RED=25, BLACK=GRD)
################################################################
# Matrix Setting
WIDTH, HEIGHT = 128, 32
################################################################
# Image Setting
fontdir = "font/"
font4 = fontdir + "pixel.ttf"
font3 = fontdir + "tiny.ttf"
font2 = fontdir + "zepto.ttf"
font_hoge = fontdir + "digital.ttf"
font = fontdir + "helv.ttf"
TIMEFONT = ImageFont.truetype( fontdir + "digital.ttf", 9)
TIMEFONT = ImageFont.truetype( fontdir + "digital.ttf", 10)
NEWSFONT = ImageFont.truetype( fontdir + "pixel.ttf", 8)
NEWSFONT2 = ImageFont.truetype(font4,7)
#NEWSFONT2 = ImageFont.truetype(font2,14)
#NEWSFONT2 = ImageFont.truetype(font5,9)
NEWSFONT3 = ImageFont.truetype(font2,8)
#NEWSFONT3 = ImageFont.truetype(font,8)
NEWSFONT4 = ImageFont.truetype(font,10)
NEWSFONT = ImageFont.load( \
    os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)) ) \
    + '/' + fontdir + 'helvR08.pil')
FONT1 = ImageFont.truetype(font, 1)
FONT2 = ImageFont.truetype(font, 2)
FONT3 = ImageFont.truetype(font, 3)
FONT4 = ImageFont.truetype(font, 4)
FONT5 = ImageFont.truetype(font, 5)
FONT6 = ImageFont.truetype(font, 6)
FONT7 = ImageFont.truetype(font, 7)
FONT8 = ImageFont.truetype(font, 8)
FONT9 = ImageFont.truetype(font, 9)
FONT10 = ImageFont.truetype(font, 10)
#FONT8 = ImageFont.truetype(font2, 8)
#FONT9 = ImageFont.truetype(font, 9)
#FONT10 = ImageFont.truetype(font3, 8)

"""
FONT1 = ImageFont.truetype(font, 2)
FONT3 = ImageFont.truetype(font, 4)
FONT4 = ImageFont.truetype(font, 5)
FONT7 = ImageFont.truetype(font, 7)
FONT8 = ImageFont.load( \
    os.path.dirname(os.path.realpath(__file__) ) \
    + '/helvR08.pil')
FONT9 = ImageFont.truetype(font, 9)
"""
FONT24 = ImageFont.truetype( fontdir + "helv.ttf", 24)
FONT16 = ImageFont.truetype( fontdir + "helv.ttf", 16)
MYFONT = lambda num:ImageFont.truetype(font, num)
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
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
################################################################
# News Setting
NEWS_INTERVAL = 300
# Weather Setting
WEATHER_INTERVAL = 1800 * 3
################################################################

class config():
    # Variables
    key_down_time = 0
    key_down_length = 0
    key_up_time = 0
    buffer = []; word = []; code = []

    # Tone Object
    tone_obj = ToneSound(frequency = 500, volume = 0.8)
    # Key Setting
    key = gpio.Button(PIN, pull_up = True)
    # Matrix Setting
    #matrix = RGBMatrix(32, 3)


    options = RGBMatrixOptions()
    options.rows = WIDTH
    options.cols = HEIGHT
    options.rows = 32
    options.cols = 128
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'

    matrix = RGBMatrix(options = options)
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
        self.width = WIDTH
        self.height = HEIGHT


    # Setter
    def set_global_status(self, status):
        self.global_status = [status]

    # Getter
    def get_global_status(self):
        return self.global_status[0]

    
