# Modules
from flask import Flask, render_template
import json

import _gpio as GPIO

# import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# GPIO setup
PINS = None
with open("pins.json") as f:
    PINS = json.load(f)

if not PINS:
    raise Exception("Pins file not found")

GPIO.setup(PINS["LED"], GPIO.OUT)

# Initial state
STATES = {"light": False}

# App setup
app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route("/")
def index():
    return render_template("index.html", led_status=STATES["light"])


# Light
@app.route("/set-light/<int:status>", methods=["POST"])
def set_light(status):
    STATES["light"] = bool(status)
    GPIO.output(PINS["LED"], STATES["light"])

    return "OK", 200


# Me testing a fake raspberry pi on my macbook
@app.route("/board")
def board():
    return GPIO.print_board()


if __name__ == "__main__":
    app.run()
