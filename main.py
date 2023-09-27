# Modules
try:
    import RPi.GPIO as GPIO
except ImportError:
    import _gpio as GPIO

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

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
        "favorites": {
            "temperature": 230,
            "humidity": 42.2,
            "light_intensity": 33333,
        },
    }

    return render_template(
        "index.html", states=STATES, sensors=SENSOR_VALUES, user=user
    )


# Favourites
@app.route("/set-favourites", methods=["POST"])
def set_favourites():
    data = request.get_json()
    print(data)

    # TODO: Save the favourites to the user's profile
    return "OK", 200


# Fan
@app.route("/set-fan/<int:status>", methods=["POST"])
def set_fan(status):
    STATES["fan"] = bool(status)

    # TODO: Activate the fans
    return "OK", 200


# Light
@app.route("/set-light/<int:status>", methods=["POST"])
def set_light(status):
    STATES["light"] = bool(status)
    GPIO.output(PINS["LED"], STATES["light"])

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3333)
