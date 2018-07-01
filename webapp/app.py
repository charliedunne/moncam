#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Garden Monitor Webserver

This is a Flask application (webserver) that provide to the user the ability to monitor a room telmatically using camera images.

Attributes:
	None

"""


from flask import Flask, render_template, session, request, flash
from picamera import PiCamera, Color
from time import sleep, gmtime, strftime
from dateutil import tz
import datetime
import time
import os
import hashlib
import pickle

app = Flask(__name__)

# Path of the images
IMG_PATH="/home/pi/moncam/webapp/static"
USER_PASS='/home/pi/moncam/webapp/private/pass_user'
ROOT_PASS='/home/pi/moncam/webapp/private/pass_root'


def get_timestamp():
    
    # Timestamp in Local Area
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Europe/Madrid')
    utc = time.gmtime()
    timestamp = datetime.datetime.now(tz.gettz("Europe/Madrid")).isoformat()

    return timestamp
    

@app.route('/')
def index():

    if not session.get('logged_in'):
        return render_template('login.html')
    else:

        # Take image
        with PiCamera() as camera:

            # Timestamp
            timestamp = get_timestamp()

            # Camera configuration parameters
            camera.resolution = (3280, 2464)
            camera.rotation = -90
            camera.shutter_speed = 0 # AUTO
            camera.annotate_text = timestamp
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

            #timestamp = strftime("%Y-%m-%d %H:%M:%S", local_timestamp)
            camera.capture(os.path.join(IMG_PATH, 'now.jpg'), quality=100, format="jpeg")
            camera.stop_preview()

            return render_template('index.html', image='now.jpg', timestamp=timestamp)

	
@app.route('/maxsnapshoot/<image>')
def maxsnapshoot(image):

    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        
        timestamp = get_timestamp()

        return render_template('maxsnapshoot.html', image=image, timestamp=timestamp)

@app.route('/login', methods=['POST'])
def authenticate():

    # Open the user hash
    f_in = open(USER_PASS, 'rb')
    user_hash = pickle.load(f_in)
    f_in.close()

    # Open the root hash
    f_in = open(ROOT_PASS, 'rb')
    root_hash = pickle.load(f_in)
    f_in.close()

    # Obtain the pasword
    clear_pwd = request.form['password']

    # MD5 the password
    md5_pwd = hashlib.md5(clear_pwd.encode('utf8')).hexdigest()

    if (md5_pwd == user_hash) or (md5_pwd == root_hash):
        session['logged_in'] = True
    else:
        flash('wrong password')
    
    return index()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()


if __name__ == '__main__':

    app.secret_key = os.urandom(12)
    # Run the Web Server
    app.run(debug=False, host='0.0.0.0', port=5000)

    
