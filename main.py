#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import threading, time

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

# Local class
from config import config
from info_thread import info_thread
from news_thread import news_thread
from input_thread import input_thread

# Main Function
def main():
    # Config class
    global myconfig
    myconfig = config()
    local_status = myconfig.get()

    # Launch Threads
    print ("starting threads")
    thread_info = info_thread(myconfig)
    thread_news = news_thread(myconfig)
    thread_input = input_thread(myconfig)

    # Lock Threads
    def lock_all():
        for thread in [ thread_info, thread_input, thread_news ]:
            thread.lock.acquire() if not thread.lock.locked() else None
    lock_all()
    thread_info.lock.release()

    # Start Threads
    thread_info.start()
    thread_news.start()
    thread_input.start()

    check_lock = lambda x: "LOCKED" if x.locked() else "NOT LOCKED"

    ### Main Section ###
    while True:
        logging.debug("global_status: " +  myconfig.get())
        logging.debug("info: " +  check_lock(thread_info.lock) + \
                      ", input: " +  check_lock(thread_input.lock) + \
                      ", news: " +  check_lock(thread_news.lock) )

        # Check config class, if change made, change state
        if local_status is not myconfig.get():
            # Lock everything
            lock_all()

            # Adjust if transition is not smooth
            time.sleep(.1)

            # State change
            local_status = myconfig.get()
            if (local_status is "info_thread"):
                thread_info.lock.release()
            elif (local_status is "input_thread"):
                thread_input.lock.release()
            else:
                thread_news.lock.release()
        # No change, no action
        else:
            time.sleep(1)
        
if __name__ == '__main__':
    main()
