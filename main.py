#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()

import atexit
import logging
import threading, time

# Local class
import sys
sys.path.insert(0, "thread")
sys.path.insert(0, "lib")
from config import config
from info_thread import info_thread
from news_thread import news_thread
from output_thread import output_thread
from AdafruitNextBus.nextbus_matrix import bus_thread
from AdafruitNextBus.predict import predict

from input_thread import input_thread
from MatrixManip import MatrixManip

from twitter_news import *
from weather import *
from weather_keys import *
#from stock import *

# Logging Setups
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


# Main Function
def main():
    # Config class
    global myconfig
    myconfig = config()
    def clearOnExit():
        myconfig.matrix.Clear()
    atexit.register(clearOnExit)
    
    local_status = myconfig.get_global_status()

    # Launch Threads
    print ("starting threads")
    ## Twitter News Thread
    twitter = threading.Thread(target=getNews)
    twitter.daemon = True
    twitter.name = "Twitter News"
    twitter.start()
    """
    # Weather Thread
    # Start thread to update weather information
    locid = weather_loc.get("Boston", weather_loc["Boston"])
    weather = threading.Thread(target=getWeather, args=(config, locid))
    weather.daemon = True
    weather.name = "Weather"
    weather.start()
    """
    '''
    # Weather Thread
    weather = threading.Thread(target=getWeather)
    weather.daemon = True
    weather.name = "Weather"
    # Stock Thread
    stock = threading.Thread(target=getStock)
    stock.daemon = True
    stock.name = "Stock"
    '''

    thread_info = info_thread(myconfig)
    thread_news = news_thread(myconfig)
    thread_output = output_thread(myconfig)
    thread_bus = bus_thread(myconfig)

    thread_input = input_thread(myconfig)

    # Lock Threads
    def lock_all():
        for thread in [ thread_info, thread_output, thread_news, thread_bus ]:
            thread.lock.acquire() if not thread.lock.locked() else None
    lock_all()

    # Start Threads
    thread_info.start()
    thread_news.start()
    thread_output.start()
    thread_bus.start()
    thread_input.start()

    thread_info.lock.release() # Also edit config to change entry state

    ### Main Section ###
    check_lock = lambda x: "LOCKED" if x.locked() else "NOT LOCKED"
    logging.debug("Ready")
    while True:

        #logging.debug("global_status: " +  myconfig.get_global_status())
        """
        logging.debug("info: " +  check_lock(thread_info.lock) + \
                      ", bus: " +  check_lock(thread_bus.lock) + \
                      ", output: " +  check_lock(thread_output.lock) + \
                      ", news: " +  check_lock(thread_news.lock) )
        """
        if local_status is not myconfig.get_global_status():
            # If config changes, state also changes
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
                thread_bus.lock.release()
            elif (local_status is "sleep"):
                lock_all()
            elif (local_status is "exit"):
                break
        # No change, no action
        else:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break
                
        
if __name__ == '__main__':
    main()
