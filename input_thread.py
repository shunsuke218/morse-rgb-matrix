#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import random
import threading, time

# Local class
from config import config

class input_thread(threading.Thread):
    # Constructor
    def __init__(self, input):
        threading.Thread.__init__(self, args=(input,))
        self.name = "input thread"
        self.lock = threading.Lock()
        self.global_status = input
        self.daemon = True

    # Main section
    def run(self):
        while True:
            # Check the state, wait if others are in progress
            self.lock.acquire()

            # Do Stuff
            while True:
                logging.debug("global: " + str(self.global_status.get()))
                num = random.randint(1,1000)
                logging.debug("num: " + str(num) + \
                              ", change? " + str((num > 500)) )
                time.sleep(.1)

                # If signal sent, change state
                if (num > 750):
                    break

            #Exitting state; change config to the next state
            decision = "info_thread" if random.randint(0,1) else "news_thread"
            logging.debug("global_status has been updated!!" + str(self.global_status.get()) + "->" +  decision)
            self.global_status.set(decision)
            time.sleep(3)
