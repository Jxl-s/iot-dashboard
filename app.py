# Modules
try:
    import RPi.GPIO as GPIO
except ImportError:
    import _gpio as GPIO

import json

from flask import Flask, render_template, request
from flask_socketio import SocketIO
from threading import Thread

# My packages
from pins import PINS, setup as pins_setup

# App setup
app = Flask(__name__, static_folder="static", template_folder="templates")
socketio = SocketIO(app, async_mode=None)

# GPIO setup
pins_setup()

# TODO: these will most likely change because of different project requirements
STATES = {"light": False, "fan": False}
SENSOR_VALUES = {
    "temperature": 10.9,
    "humidity": 57.5349,
    "light_intensity": 9302,
    "devices": 32,
}
USER = {
    "name": "Jiaxuanli_123",
    "description": "The main user of this computer",
    "avatar": "/static/images/default-user.jpg",
    "favourites": {
        "temperature": 20.4,
        "humidity": 42.2,
        "light_intensity": 4722,
    },
}


# Dashboard page
@app.route("/")
def index():
    return render_template("index.html")


# Gets the initial page data
@app.route("/get-data")
def get_data():
    # TODO: Check if the user is logged in, through request cookies or a session.

    # If they are logged in, get their data from the database, otherwise
    # use False as user.
    response = json.dumps({"states": STATES, "sensors": SENSOR_VALUES, "user": USER})
    return response, 200, {"Content-Type": "application/json"}


# Changes the user's preference
@app.route("/set-favourites", methods=["POST"])
def set_favourites():
    # TODO: Check if the user is logged in, only update their entries
    data = request.get_json()

    # Make sure fields are present
    if not data["temperature"] or not data["humidity"] or not data["light"]:
        return "Missing data", 400

    # Make sure fields are valid
    if not isinstance(data["temperature"], (int, float)):
        return "Invalid temperature", 400

    if not isinstance(data["humidity"], (int, float)):
        return "Invalid humidity", 400

    if not isinstance(data["light"], (int, float)):
        return "Invalid light", 400

    # Save the favourites to the array
    USER["favourites"]["temperature"] = data["temperature"]
    USER["favourites"]["humidity"] = data["humidity"]
    USER["favourites"]["light_intensity"] = data["light"]

    # TODO: Save the favourites to the user's profile in the future
    return "OK", 200


# Fan
@socketio.on("set_fan")
def set_fan(status):
    STATES["fan"] = bool(status)

    # TODO: Activate the fans

    socketio.emit("fan_update", STATES["fan"])


# Light
@socketio.on("set_light")
def set_light(status):
    STATES["light"] = bool(status)
    GPIO.output(PINS["LED"], STATES["light"])

    socketio.emit("light_update", STATES["light"])


# TODO: remove this, and actually listen to sensor changes
# this will also most likely be gone because of project requirements
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
    # TODO: use the real sensor function
    Thread(target=send_dummy_data).start()
    app.run(host="0.0.0.0", port=3333)
