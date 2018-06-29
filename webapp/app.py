from flask import Flask, render_template, session, request, flash
from picamera import PiCamera
from time import sleep, gmtime, strftime
from dateutil import tz
import datetime
import time
import os

app = Flask(__name__)

# Path of the images
IMG_PATH="/home/pi/moncam/webapp/static"

@app.route('/')
def index():

    if not session.get('logged_in'):
        return render_template('login.html')
    else:

        # Take image
        with PiCamera() as camera:

            # Camera configuration parameters
            camera.resolution = (3280, 2464)
            camera.rotation = -90
            camera.shutter_speed = 0 # AUTO
            camera.exposure_mode = 'night'
            sleep(1);

            from_zone = tz.gettz('UTC')
            to_zone = tz.gettz('Europe/Madrid')
            utc = time.gmtime()
            timestamp = datetime.datetime.now(tz.gettz("Europe/Madrid")).isoformat()
            #timestamp = strftime("%Y-%m-%d %H:%M:%S", local_timestamp)
            camera.capture(os.path.join(IMG_PATH, 'now.jpg'))

            return render_template('index.html', image='now.jpg', timestamp=timestamp)

	
@app.route('/maxsnapshoot/<image>')
def maxsnapshoot(image):

    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('maxsnapshoot.html', image=image)

@app.route('/login', methods=['POST'])
def authenticate():
    if request.form['password'] == 'admin':
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

    
