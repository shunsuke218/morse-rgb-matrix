#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import threading, time

# Local class
from config import *
from MatrixManip import *
from twitter_news import *

class news_thread(threading.Thread):
    # Constructor
    def __init__(self, input):
        threading.Thread.__init__(self, args=(input,))
        self.name = "news thread"
        self.lock = threading.Lock()
        self.global_status = input
        self.daemon = True
        # Config
        self.config = input
        self.matrix_manip = MatrixManip(self.config)

    # Main section
    def run(self):
        while True:
            # Check the state, wait if others are in progress
            self.lock.acquire()
            # Clean Matrix
            self.matrix_manip.MatrixPrintDelete()
            local_word = config.word[:]
            no_action = time.time()

            # Do Stuff
            while True:
                # Check if state has changed
                if self.config.get_global_status() is not "news_thread": break
                if config.news:
                    for news in config.news:
                        logging.debug(news)
                        if self.config.get_global_status() is not "news_thread":
                            self.matrix_manip.MatrixPrintDelete()
                            break
                        self.matrix_manip.MatrixPrintStr(news)
                        time.sleep(2)
                        self.matrix_manip.MatrixPrintDelete()
                    time.sleep(3)

            # State changed; Clean up before sleep
            self.matrix_manip.MatrixPrintDelete()
            #self.global_status.set_global_status("output_thread")
            time.sleep(1)
