#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Capture PiCam

This script is in charge of capturing a single frame (image) using PiCam, place
in the appropriate path with the specified filename so the web application
'moncam' was able to read it.

Example:
	$ python3 capture.py


Attributes:
	None

"""

from picamera import PiCamera
from time import sleep, gmtime, strftime
from dateutil import tz
import time
import datetime
import os


IMG_PATH="/home/pi/moncam/webapp/static"

def main():
    """Main function
    
    1. Select the appropriate filename depending on the current time
    2. Capture a image
    """

    # Current timestamp (Europe/Madrid Time)
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Europe/Madrid')
    utc = time.gmtime()
    timestamp = datetime.datetime.now(tz.gettz("Europe/Madrid"))
    
    filename = strftime("T" + str(timestamp.hour).zfill(2) + "00.jpg")

    with PiCamera() as camera:

        # Camera configuration parameters
        camera.resolution = (3280, 2464)
        camera.rotation = -90
        camera.shutter_speed = 0 # AUTO
        camera.exposure_mode = 'night'
        sleep(1);

        # Take the image
        camera.capture(os.path.join(IMG_PATH, filename))

if __name__ == '__main__':

    # Run the program
    main()


