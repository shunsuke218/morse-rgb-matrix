#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import threading, time

# Local class
from config import *
from MatrixManip import *

class output_thread(threading.Thread):
    # Constructor
    def __init__(self, output):
        # Thread settings
        threading.Thread.__init__(self, args=(output,))
        self.name = "output thread"
        self.daemon = True
        self.lock = threading.Lock()
        # Config
        self.config = output
        self.matrix_manip = MatrixManip(self.config)

    # Main section
    def run(self):
        #MatrixPrintStr("HR HR BT")
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
                if self.config.get_global_status() is not "output_thread": break
                # Check if no input for 60 seconds
                if no_action - time.time() > 30:
                    self.config.set_global_status("info_thread"); break
                    
                # Check if word has updated
                if not local_word == config.word:
                    no_action = time.time()
                    if len(local_word) < len(config.word):
                        # Word added
                        self.matrix_manip.MatrixPrintChar(config.word[-1], config.code[-1])
                    else:
                        # Word deleted
                        self.matrix_manip.MatrixPrintDelete()
                    # Update word
                    local_word = config.word[:]
                time.sleep(1)

            # State changed; Clean up before sleep
            self.matrix_manip.MatrixPrintDelete()
            time.sleep(1)
