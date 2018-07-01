# moncam
Monitor remotely one place using Raspberry pi and PiCamera

<h2>Introduction</h2>

It is just a simple web application created using python Flask that allows to monitor stills taken by the PiCamera in your web browser.

The initial version provide the following features:

<nl>
	<li>Security access. Single user password for access</li>
	<li>New still from PiCam is taken with every refresh of the webpage</li>
	<li>Time-tagged thumbail of the last image taken</li>
	<li>Posibility to enlarge to full resolution by cliking into the image or in its timetag</li>
	<li>History of images taken every hour during the day</li>
</nl>

<h2>Installation</h2>

There is no installation script, the process must be addressed manually following hereafter instructions:

<h3>HW Prerequisites</h3>

List of Hardware elements that are required for the installation:

<nl>
	<li>Raspberry Pi. Recomended rPi Zero W</li>
	<li>PiCamera V2 (8 Mpx) and ribbon cable</li>
	<li>Power Supply</li>
</nl>

<h3>SW Prerequisites</h3>

List of SW that is required for the configuration of the system.

<nl>
	<li>Raspbian. Lite version is enough</li>
	<li>Python3</li>
	<li>Flask</li>
	<li>SSH Access</li>
	<li>Cron</li>

</nl>

<h3>Procedure</h3>

The subsystem is composed by two applications: The first and main one is <b>moncam/webapp/app.py</b> that is the web server. The other one is a small python script <b>/moncam/capture/capture.py</b> that is in charge of taking stills for the recod history.

You can run each of those applications manually but ideally they should be executed automatically on start-up. 

<h4>Webserver</h4>
For the case of the webserver the simplest option is to include a line for its execution in the <i>/etc/rc.local</i> so it was executed during start-up.

Add the following line before the 'exit 0' in your <i>/etc/rc.local</i>:
<code>
# Run FLASK server
/usr/bin/python3 /home/pi/moncam/webapp/app.py > /var/log/flask.log 2>&1 &
</code>

This shall run the webserver at the end of the boot procedure and place some useful login in the path <i>/var/log/flask.log</i>

<h5>Capture</h5>
The capture system shall take stills, tipically every hour, to be available as historic information in the web application.

To configure that just use the cron and execute this python script every hour. You can use the following command in the crontab:

<code>
# Run The Capture (one image for each hour of the day)
00 * * * * /usr/bin/python3 /home/pi/moncam/capture/capture.py
</code>

<h6>Create Password for User</h6>

Clean installation does not include any password registered so there is no way to authenticate in the web server until you create a password hash. To create it there is a small python script that make it for you <b>~/moncam/webapp/private/generate_password.py</b>. Just type in your console:

<code>
$ python3 generate_password.py
</code>

And type your password when asked. This script shall create a file <b>pass_user</b> that contain the hash of the password to be compared with in the login procedure

<b>IMPORTANT</b> For security reasons it is highliy recomended that you modify the permissions of the file <b>pass_user</b> and even the <b>private</b> folder so the only read and write permissions are awolled to the <b>pi</b> user.

<h2>How to Use</h2>
Once installed just connect to your raspberry ip using the port 5000 in your browser. Type your password in the dialog and, after a while, note that the process of capturing stills take like 5 seconds, you will be able to see the main page.