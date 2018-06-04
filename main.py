#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()

import atexit
import logging
import threading, time

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

# Local class
from config import config
from info_thread import info_thread
from news_thread import news_thread
from output_thread import output_thread

from input_thread import input_thread


# Main Function
def main():
    # Config class
    global myconfig
    myconfig = config()
    #myconfig.key = gpio.Button(self.pin, pull_up = True)
    def clearOnExit():
        myconfig.matrix.Clear()
    atexit.register(clearOnExit)

    
    local_status = myconfig.get_global_status()

    # Launch Threads
    print ("starting threads")
    thread_info = info_thread(myconfig)
    thread_news = news_thread(myconfig)
    thread_output = output_thread(myconfig)

    thread_input = input_thread(myconfig)

    # Lock Threads
    def lock_all():
        for thread in [ thread_info, thread_output, thread_news ]:
            thread.lock.acquire() if not thread.lock.locked() else None
    lock_all()
    thread_output.lock.release()

    # Start Threads
    thread_info.start()
    thread_news.start()
    thread_output.start()

    thread_input.start()


    ### Main Section ###
    check_lock = lambda x: "LOCKED" if x.locked() else "NOT LOCKED"
    while True:
        logging.debug("global_status: " +  myconfig.get_global_status())
        logging.debug("info: " +  check_lock(thread_info.lock) + \
                      ", output: " +  check_lock(thread_output.lock) + \
                      ", news: " +  check_lock(thread_news.lock) )
        # Check config class, if change made, change state
        if local_status is not myconfig.get_global_status():
            logging.debug("status changed!!!")
            # Lock everything
            lock_all()

            # Adjust if transition is not smooth
            time.sleep(.1)

            # State change
            local_status = myconfig.get_global_status()
            if (local_status is "info_thread"):
                thread_info.lock.release()
            elif (local_status is "output_thread"):
                thread_output.lock.release()
            elif (local_status is "news_thread"):
                thread_news.lock.release()
            elif (local_status is "bus_thread"):
                thread_news.lock.release()
            elif (local_status is "sleep"):
                lock_all()
            elif (local_status is "exit"):
                break
        # No change, no action
        else:
            time.sleep(1)
        
if __name__ == '__main__':
    main()
