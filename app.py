from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room
import RPi.GPIO as gpio

pins = [22, 24, 23, 25] #[w, a, s, d]
# These pins are connected to a relay module which is connected to the cars remote control. The relay simulates a button press

gpio.setmode(gpio.BCM)
gpio.setup(pins, gpio.OUT)
gpio.output(pins, True)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'why would I put my secret key on github?'
socketio = SocketIO(app)

@app.route('/')
def controller():
	return render_template('index.html')

@socketio.on('pressedButtons')
def handle_json(json):
	print('received:', str(json))
	if json['w'] is True:
		gpio.output(pins[0], False)
	else:
		gpio.output(pins[0], True)
	if json['a'] is True:
		gpio.output(pins[1], False)
	else:
		gpio.output(pins[1], True)
	if json['s'] is True:
		gpio.output(pins[2], False)
	else:
		gpio.output(pins[2], True)
	if json['d'] is True:
		gpio.output(pins[3], False)
	else:
		gpio.output(pins[3], True)

if __name__ == '__main__':
	try:
		socketio.run(app, host='192.168.1.174', port=5000)
	except KeyboardInterrupt:
		gpio.cleanup()
		print('exiting')
