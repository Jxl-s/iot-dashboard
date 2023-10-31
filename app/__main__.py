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
from utils.database import get_user_by_id
from utils.freenove_dht import DHT

# Load env, and setup the email client
load_dotenv()
email_client = EmailClient(os.environ["EMAIL_ADDRESS"], os.environ["EMAIL_PASSWORD"])

# App setup
app = Flask(__name__, static_folder="../static")
socketio = SocketIO(app, async_mode=None)

# GPIO setup
pins_setup()

dht = DHT(PINS["DHT11"])
STATES = {"light": GPIO.input(PINS["LED"]), "fan": GPIO.input(PINS["MOTOR_EN"])}

SENSOR_VALUES = {
    "temperature": 0,
    "humidity": 0,
    "light_intensity": 1000,
    "devices": 0,
}

# Set the initial values of DHT11
print("[Main] Reading DHT11...")
if dht.readDHT11() == dht.DHTLIB_OK:
    print("[Main] Got DHT11 Value")

    SENSOR_VALUES["temperature"] = dht.temperature
    SENSOR_VALUES["humidity"] = dht.humidity
else:
    print("[Main] Failed to read DHT11 Value")

# email to which to send emails
NOTIFICATION_EMAIL = os.environ["NOTIFICATION_EMAIL"]

# Load the user account (0 will indicate no logged in user)
# TODO: Make this with the RFID reader

user_id = 1
user_info = get_user_by_id(user_id)


# Dashboard page
@app.route("/")
def index():
    return send_file("../static/index.html")


# Gets the initial page data
@app.route("/get-data")
def get_data():
    # If they are not logged in, use False as user.
    response = json.dumps(
        {"states": STATES, "sensors": SENSOR_VALUES, "user": user_info}
    )
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
    user_info["favourites"]["temperature"] = data["temperature"]
    user_info["favourites"]["humidity"] = data["humidity"]
    user_info["favourites"]["light_intensity"] = data["light"]

    # TODO: Save the favourites to the user's profile in the future
    return "OK", 200


# Fan
@socketio.on("set_fan")
def set_fan(status):
    STATES["fan"] = bool(status)

    GPIO.output(PINS["MOTOR_EN"], STATES["fan"])
    GPIO.output(PINS["MOTOR_IN1"], GPIO.LOW)  # This will be off for now
    GPIO.output(PINS["MOTOR_IN2"], STATES["fan"])

    socketio.emit("fan_update", STATES["fan"])


# Light
@socketio.on("set_light")
def set_light(status):
    STATES["light"] = bool(status)
    GPIO.output(PINS["LED"], STATES["light"])

    socketio.emit("light_update", STATES["light"])


# This thread handles sensors
def sensor_thread():
    while True:
        # Make sure the DHT11 is working
        if dht.readDHT11() == dht.DHTLIB_OK:
            SENSOR_VALUES["temperature"] = dht.temperature
            SENSOR_VALUES["humidity"] = dht.humidity

        # TODO: Use the real values for light intensity and devices
        SENSOR_VALUES["light_intensity"] = 1000
        SENSOR_VALUES["devices"] = 0

        socketio.emit("sensor_update", SENSOR_VALUES)
        time.sleep(1)


# This thread handles email-related actions
def email_thread():
    # How much time before re-sending an email
    EMAIL_TIMEOUT = 60 * 2  # 2 minutes

    # Indicates whether the email has already been sent, to prevent spamming
    email_cooldown = {
        "temperature": 0,
    }

    while True:
        cur_time = time.time()

        # Handle temperature
        temp = SENSOR_VALUES["temperature"]
        prefered_temp = user_info["favourites"]["temperature"]

        if (
            temp > prefered_temp
            and email_cooldown["temperature"] <= cur_time
            and not STATES["fan"]
        ):
            # Send the email
            email_cooldown["temperature"] = cur_time + EMAIL_TIMEOUT
            email_client.send_temp_email(NOTIFICATION_EMAIL, temp, prefered_temp)

            print("[Main] Sent temperature email")

        # Check for a response from the temperature
        response = email_client.check_temp_res(NOTIFICATION_EMAIL)
        if response:
            print("[Main] User responded with YES")
            set_fan(True)

        # Don't abuse the email server
        time.sleep(5)


if __name__ == "__main__":
    # TODO: use the real sensor function
    Thread(target=sensor_thread).start()
    Thread(target=email_thread).start()

    app.run(host="0.0.0.0", port=3333)
