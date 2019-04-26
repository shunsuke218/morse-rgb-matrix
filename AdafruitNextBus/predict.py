# NextBus prediction class.  For each route/stop, NextBus server is polled
# automatically at regular intervals.  Front-end app just needs to init
# this with stop data, which can be found using the routefinder.py script.

import threading
import time
import urllib.request
from xml.dom.minidom import parseString
import logging
import json
from datetime import datetime
import requests
from mbta_keys import *

import json

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


class predict:
    interval  = 120 # Default polling interval = 2 minutes
    initSleep = 0   # Stagger polling threads to avoid load spikes

    # predict object initializer.  1 parameter, a 4-element tuple:
    # First element is agengy tag (e.g. 'actransit')
    # Second is line tag (e.g. '210')
    # Third is stop tag (e.g. '0702630')
    # Fourth is direction -- not a tag, this element is human-readable
    # and editable (e.g. 'Union Landing') -- for UI purposes you may
    # want to keep this short.  The other elements MUST be kept
    # verbatim as displayed by the routefinder.py script.
    # Each predict object spawns its own thread and will perform
    # periodic server queries in the background, which can then be
    # read via the predictions[] list (est. arrivals, in seconds).
    def __init__(self, data):
        self.data          = data
        self.predictions   = []
        self.lastQueryTime = time.time()
        t                  = threading.Thread(target=self.thread)
        t.daemon           = True
        self.command = ''
        t.start()

    # Periodically get predictions from server ---------------------------
    def thread(self):
        initSleep          = predict.initSleep
        predict.initSleep += 5   # Thread staggering may
        time.sleep(initSleep)    # drift over time, no problem
        while True:
                """
                self.command = 'predictions' + \
                '&a=' + self.data[0] +   \
                '&r=' + self.data[1] +   \
                '&s=' + self.data[2]    # Stop
                """
                self.command = "departure_time" + \
                               "&filter%5Bstop%5D=" + self.data[2] + \
                               "&filter%5Broute%5D=" + self.data[1]
                jsondata = predict.req(self.command)
                if jsondata is None: return     # Connection error
                self.lastQueryTime = time.time()
                predictions = jsondata["data"]
                #predictions = jsondata.getElementsByTagName('prediction')
                newList     = []
                for p in predictions:      # Build new prediction list
                    arrtime_string = p["attributes"]["arrival_time"][:-6]
                    arrtime = datetime.strptime(arrtime_string, '%Y-%m-%dT%H:%M:%S')
                    newList.append((arrtime - datetime.now()).total_seconds())
                    #newList.append(int(p.getAttribute('seconds')))
                self.predictions = newList # Replace current list
                time.sleep(predict.interval)

    # Open URL, send request, read & parse XML response ------------------
    @staticmethod
    def req(cmd):
        xml = None
        jsondata = None
        try:
            header = {"accept": "application/vnd.api+json"}
            req = urllib.request.Request(url="https://api-v3.mbta.com" +\
                                         "/predictions?sort=" + cmd, \
                                         method="GET")
                                         #headers=header, method="GET")
            connection = urllib.request.urlopen(req, timeout=20)

            """
            connection = urllib.request.urlopen(
              'http://webservices.nextbus.com'  +
              '/service/publicXMLFeed?command=' + cmd)
            """
            raw = connection.read().decode('utf8')
            connection.close()
            jsondata = json.loads(raw)
            #json = json.loads(raw)
            #xml = parseString(raw)
        finally:
            return jsondata

    # Set polling interval (seconds) -------------------------------------
    @staticmethod
    def setInterval(i):
        interval = i

    def toString(self):
            return "https://api-v3.mbta.com" + \
                "/predictions?sort=" + self.command
