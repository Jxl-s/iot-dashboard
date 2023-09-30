# Modules
try:
    import RPi.GPIO as GPIO
except ImportError:
    import _gpio as GPIO

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from threading import Thread

import json
import filters

# App setup
app = Flask(__name__, static_folder="static", template_folder="templates")
socketio = SocketIO(app, async_mode=None)

app.jinja_env.filters["number_with_commas"] = filters.number_with_commas
app.jinja_env.filters["round_two_decimals"] = filters.round_two_decimals

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PINS = None
with open("pins.json") as f:
    PINS = json.load(f)

if not PINS:
    raise Exception("Pins file not found")

GPIO.setup(PINS["LED"], GPIO.OUT)

STATES = {"light": False, "fan": False}
SENSOR_VALUES = {
    "temperature": 10.9,
    "humidity": 57.5349,
    "light_intensity": 9302,
    "devices": 32,
}


# App routes
@app.route("/")
def index():
    # TODO: Check if the user is logged in, through request cookies or a session.

    # If they are logged in, get their data from the database, otherwise
    # use False as user.

    # Temporary data to test with
    user = {
        "name": "Jiaxuanli_123",
        "description": "The main user of this computer",
        "avatar": "/static/images/default-user.jpg",
        "favourites": {
            "temperature": 20.4,
            "humidity": 42.2,
            "light_intensity": 4722,
        },
    }

    return render_template(
        "index.html", states=STATES, sensors=SENSOR_VALUES, user=user
    )


# Favourites
@app.route("/set-favourites", methods=["POST"])
def set_favourites():
    data = request.get_json()

    # TODO: Save the favourites to the user's profile
    return "OK", 200


# Fan
@socketio.on('set_fan')
def set_fan(status):
    STATES["fan"] = bool(status)

    # TODO: Activate the fans

    socketio.emit("fan_update", STATES["fan"])


# Light
@socketio.on('set_light')
def set_light(status):
    STATES["light"] = bool(status)
    GPIO.output(PINS["LED"], STATES["light"])

    socketio.emit("light_update", STATES["light"])

# TODO: remove this, and actually listen to sensor changes
def send_dummy_data():
    import random
    import time

    while True:
        SENSOR_VALUES["temperature"] = random.randint(10, 30)
        SENSOR_VALUES["humidity"] = random.randint(30, 80)
        SENSOR_VALUES["light_intensity"] = random.randint(1000, 10000)
        SENSOR_VALUES["devices"] = random.randint(0, 50)

        socketio.emit("sensor_update", SENSOR_VALUES)
        time.sleep(0.5)


if __name__ == "__main__":
    # TODO: use the actuatly sensor function
    Thread(target=send_dummy_data).start()
    app.run(host="0.0.0.0", port=3333)
