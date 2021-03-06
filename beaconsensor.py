#!/usr/bin/env python

#Hubitat BLE Beacon Presence Detection Script

import sys
import time
import requests
import logging
import logging.handlers
sys.path.append('/usr/local/bin/blescanner')
import blescan

import bluetooth._bluetooth as bluez

LOG_FILENAME = "/var/log/blescanner.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)

# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
        def __init__(self, logger, level):
                """Needs a logger and a logger level."""
                self.logger = logger
                self.level = level

        def write(self, message):
                # Only log if there is a message (not just a new line)
                if message.rstrip() != "":
                        self.logger.log(self.level, message.rstrip())

# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger(logger, logging.ERROR)

print "All setup, here we go!"

dev_id = 0
try:
        sock = bluez.hci_open_dev(dev_id)
        print "ble thread started"


except:
        print "error accessing bluetooth device..."
        sys.exit(1)


blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

# Array elements are 'Pretty Name', 'Beacon MAC or UUID (MAC should use lower case letters)', 'hubitat device ID', and the last 0 is a counter to track departures
scanningFor = [['','','',0],\
                ['','','',0],\
                ['','','',0]]
hubitatIP = "0.0.0.0"
makerDev = "" # set this to the device number of the Maker API instance in hubitat
makerToken = "" # Set this to the Maker API Token

while True:
        returnedList = blescan.parse_events(sock, 10)
        for beacon in returnedList:
            for element in scanningFor:            
                value = beacon.find(element[1])
                if value > -1:
                    try:
                        requests.get('http://'+hubitatIP+'/apps/api/'+makerDev+'/devices/'+element[2]+'/arrived?access_token='+makerToken)
                        element[3] = 0
                    except:
                        print "Something went wrong with the Hubitat Connection, couldn't set "+element[0]+" to arrived. will keep trying..."
                elif value <= -1:
                    element[3] += 1
                if  element[3] == 2000: #this comes out to about a minute of not seeing the beacon, mark it departed
                    try:
                        requests.get('http://'+hubitatIP+'/apps/api/'+makerDev+'/devices/'+element[2]+'/departed?access_token='+makerToken)
                    except:
                        print "Something went wrong with the Hubitat Connection, couldn't set "+element[0]+" to departed. will keep trying..."
                if element[3] >= 2500:
                    element[3] = 0
