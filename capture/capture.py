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

from picamera import PiCamera, Color
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
        camera.annotate_text = timestamp.isoformat()
        camera.annotate_background = Color('white')
        camera.annotate_foreground = Color('black')
        camera.annotate_text_size = 50
        camera.iso = 0
        #camera.drc_strength = 'high'
        camera.brightness = 50
        #camera.contrast = 10
        camera.exposure_mode = 'auto'
        camera.sensor_mode = 2
        camera.framerate = 1
        camera.meter_mode = 'matrix'
        #camera.sharpness = -50
        camera.still_stats = True
        #camera.awb_mode = 'sunlight'
        camera.start_preview()
        sleep(2);

        # Take the image
        camera.capture(os.path.join(IMG_PATH, filename))

        camera.stop_preview()

if __name__ == '__main__':

    # Run the program
    main()


