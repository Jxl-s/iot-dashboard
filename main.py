# Modules
try:
    import RPi.GPIO as GPIO
except ImportError:
    import _gpio as GPIO

from flask import Flask, render_template
import json

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# GPIO setup
PINS = None
with open("pins.json") as f:
    PINS = json.load(f)

if not PINS:
    raise Exception("Pins file not found")

GPIO.setup(PINS["LED"], GPIO.OUT)

STATES = {"light": False}

# App setup
app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route("/")
def index():
    return render_template("index.html", states=STATES)


# Light
@app.route("/set-light/<int:status>", methods=["POST"])
def set_light(status):
    STATES["light"] = bool(status)
    GPIO.output(PINS["LED"], STATES["light"])

    return "OK", 200


if __name__ == "__main__":
    app.run()
