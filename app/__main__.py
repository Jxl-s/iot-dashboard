# Modules
try:
    import RPi.GPIO as GPIO
except ImportError:
    import Mock.GPIO as GPIO

import json
import os
import time

from flask import Flask, request, send_file
from flask_socketio import SocketIO
from threading import Thread

# My packages
from pins import PINS, setup as pins_setup

from dotenv import load_dotenv

from utils.email import EmailClient

# Load env, and setup the email client
load_dotenv()
email_client = EmailClient(os.environ["EMAIL_ADDRESS"], os.environ["EMAIL_PASSWORD"])

# App setup
app = Flask(__name__, static_folder="../static")
socketio = SocketIO(app, async_mode=None)

# GPIO setup
pins_setup()

# TODO: these will most likely change because of different project requirements
STATES = {"light": False, "fan": False}
SENSOR_VALUES = {
    "temperature": 22,
    "humidity": 57.53,
    "light_intensity": 400,
    "devices": 0,
}

USER = {
    "name": "computer_user_123",
    "email": "me@meeeee.com",
    "description": "The main user of this computer",
    "avatar": "/static/images/default-user.jpg",
    "favourites": {
        "temperature": 10,
        "humidity": 40,
        "light_intensity": 4000,
    },
}


# Dashboard page
@app.route("/")
def index():
    return send_file("../static/index.html")


# Gets the initial page data
@app.route("/get-data")
def get_data():
    # If they are not logged in, use False as user.
    response = json.dumps({"states": STATES, "sensors": SENSOR_VALUES, "user": USER})
    return response, 200, {"Content-Type": "application/json"}


# Changes the user's preference.
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

    GPIO.output(PINS["MOTOR_EN"], STATES["fan"])
    GPIO.output(PINS["MOTOR_IN1"], GPIO.LOW) # This will be off for now
    GPIO.output(PINS["MOTOR_IN2"], STATES["fan"])

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

    while True:
        SENSOR_VALUES["temperature"] = random.randint(10, 30)
        SENSOR_VALUES["humidity"] = random.randint(30, 80)
        SENSOR_VALUES["light_intensity"] = random.randint(1000, 10000)
        SENSOR_VALUES["devices"] = random.randint(0, 50)

        socketio.emit("sensor_update", SENSOR_VALUES)
        time.sleep(2)


# This thread handles email-related actions
def email_thread():
    # How much time before re-sending an email
    EMAIL_TIMEOUT = 60 * 2  # 2 minutes

    # Indicates whether the email has already been sent, to prevent spamming
    email_cooldown = {
        "temperature": 0,
        "light_intensity": 0,
    }

    while True:
        cur_time = time.time()

        # Handle light intensity
        light = SENSOR_VALUES["light_intensity"]
        prefered_light = USER["favourites"]["light_intensity"]

        if light < prefered_light and email_cooldown["light_intensity"] <= cur_time:
            # Change the light
            set_light(True)

            # Send the email
            email_cooldown["light_intensity"] = cur_time + EMAIL_TIMEOUT
            email_client.send_light_email(USER["email"])

            print("Sent light email!")

        # Handle temperature
        temp = SENSOR_VALUES["temperature"]
        prefered_temp = USER["favourites"]["temperature"]

        if temp > prefered_temp and email_cooldown["temperature"] <= cur_time:
            # Send the email
            email_cooldown["temperature"] = cur_time + EMAIL_TIMEOUT
            email_client.send_temp_email(USER["email"], temp, prefered_temp)

            print("Sent temperature email!")

        # Check for a response from the temperature
        response = email_client.check_temp_res(USER["email"])
        if response:
            print("User responded with YES")
            set_fan(True)

        # Delay the loop
        time.sleep(1)


if __name__ == "__main__":
    # TODO: use the real sensor function
    Thread(target=send_dummy_data).start()
    Thread(target=email_thread).start()

    app.run(host="0.0.0.0", port=3333)
