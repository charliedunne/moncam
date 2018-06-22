from flask import Flask, render_template
from picamera import PiCamera
from time import sleep

app = Flask(__name__)

@app.route('/')
def index():

    # Take image
    with PiCamera() as camera:

        # Camera configuration parameters
        camera.resolution = (3280, 2464);
        camera.rotation = 0
        camera.shutter_speed = 0 # AUTO
        camera.exposure_mode = 'night'

        camera.capture('./static/testing.jpg')

    return render_template('snapshoot.html', image='testing.jpg')

@app.route('/maxsnapshoot/<image>')
def maxsnapshoot(image):
    return render_template('maxsnapshoot.html', image=image)



if __name__ == '__main__':

    # Run the Web Server
    app.run(debug=True, host='0.0.0.0')

    
