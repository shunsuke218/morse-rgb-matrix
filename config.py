#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rgbmatrix import RGBMatrix
from PIL import Image, ImageDraw, ImageFont
import gpiozero as gpio

class config():
    # Variables
    key_down_time = 0
    key_down_length = 0
    key_up_time = 0
    buffer = []; word = []; code = []

    ################################################################
    # Morse Code Setting
    MINKEYLENGTH = .1# .07 # Minimum dit
    KEYLENGTH = .18 #dit-doh boundary
    WORDLENGTH = .90 # Word boundary
    SLEEPLENGTH = 2 # Goto Sleep
    DOT = "."
    DASH = "-"    
    ################################################################
    # Key Setting
    PIN = 25
    key = gpio.Button(PIN, pull_up = True)
    
    ################################################################
    # Matrix Setting
    WIDTH, HEIGHT = 64, 32
    matrix = RGBMatrix(32, 2)
    ################################################################
    FONT24 = ImageFont.truetype("helv.ttf", 24)
    FONT9 = ImageFont.truetype("helv.ttf", 9)
    image = Image.new('RGB', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    
    # Constructor
    def __init__(self):
        self.global_status = ["output_thread"]

    # To String
    def __str__(self):
        return str(self.global_status)

    # Setter
    def set_global_status(self, status):
        self.global_status = [status]


    # Getter
    def get_global_status(self):
        return self.global_status[0]

    
