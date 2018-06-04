#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import random
import threading, time

# Local class
from config import config

class info_thread(threading.Thread):
    # Constructor
    def __init__(self, input):
        threading.Thread.__init__(self, args=(input,))
        self.name = "info thread"
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
                logging.debug("global: " + str(self.global_status.get_global_status()))
                num = random.randint(1,1000)
                logging.debug("num: " + str(num) + \
                              ", change? " + str((num > 500)) )
                time.sleep(.1)

                # If signal sent, change state
                if (num > 500):
                    break

            # Exitting state; change config to the next state
            logging.debug("global_status has been updated!!" + str(self.global_status.get_global_status()) + " -> " + "input_thread")
            self.global_status.set_global_status("input_thread")
            time.sleep(3)
