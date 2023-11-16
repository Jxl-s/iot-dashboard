# Modules
try:
    import RPi.GPIO as GPIO
except ImportError:
    import Mock.GPIO as GPIO

import json
import os
import time
import bluetooth

from flask import Flask, request, send_file
from flask_socketio import SocketIO
from threading import Thread

# My packages
from pins import PINS, setup as pins_setup

from dotenv import load_dotenv

from utils.email import EmailClient
from utils.mqtt import MQTTClient
from utils.database import get_user_by_id, get_user_id_from_tag, update_user_favourites
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
    "light_intensity": None,
    "devices": 0,
}

CONFIG_VALUES = {"rssi_threshold": -50}

# Set the initial values of DHT11
print("[Main] Reading DHT11...")
if dht.readDHT11() == dht.DHTLIB_OK:
    print("[Main] Got DHT11 Value")

    SENSOR_VALUES["temperature"] = dht.temperature
    SENSOR_VALUES["humidity"] = dht.humidity
else:
    print("[Main] Failed to read DHT11 Value")

# Email to which to send emails
NOTIFICATION_EMAIL = os.environ["NOTIFICATION_EMAIL"]

# Load the user account (0 will indicate no logged in user)
# TODO: Make this with the RFID reader

user_id = 0
user_info = get_user_by_id(user_id)


# Updates the logged in user
def update_user(new_user_id):
    global user_id, user_info

    user_id = new_user_id
    user_info = get_user_by_id(user_id)

    socketio.emit("user_update", user_info)
    print("[Main] Updated user to", user_id, user_info)


# Utility function for clamping
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


# Dashboard page
@app.route("/")
def index():
    return send_file("../static/index.html")


# Gets the initial page data
@app.route("/get-data")
def get_data():
    # If they are not logged in, use False as user.
    response = json.dumps(
        {
            "states": STATES,
            "sensors": SENSOR_VALUES,
            "user": user_info,
            "config": CONFIG_VALUES,
        }
    )
    return response, 200, {"Content-Type": "application/json"}


# Handle logout
@app.route("/logout", methods=["POST"])
def logout():
    # User with ID 0 does not exist, so the profile will be None
    update_user(0)
    return "OK", 200


# TODO: Remove when RFID is implemented
@app.route("/login/<int:user_id>", methods=["POST"])
def login(user_id):
    update_user(user_id)
    return "OK", 200


# Changes the user's preference.
@app.route("/set-favourites", methods=["POST"])
def set_favourites():
    data = request.get_json()

    # Make sure fields are present
    if data["temperature"] is None or data["humidity"] is None or data["light"] is None:
        return "Missing data", 400

    # Make sure fields are valid
    if not isinstance(data["temperature"], (int, float)):
        return "Invalid temperature", 400

    if not isinstance(data["humidity"], (int, float)):
        return "Invalid humidity", 400

    if not isinstance(data["light"], (int, float)):
        return "Invalid light", 400

    # Save the favourites
    if user_info:
        user_info["favourites"]["temperature"] = clamp(data["temperature"], -20, 50)
        user_info["favourites"]["humidity"] = clamp(data["humidity"], 0, 100)
        user_info["favourites"]["light_intensity"] = clamp(data["light"], 0, 1024)

        # Update the user
        update_user_favourites(user_id, user_info["favourites"])

    return user_info["favourites"], 200, {"Content-Type": "application/json"}


@app.route("/set-rssi", methods=["POST"])
def set_rssi():
    data = request.get_json()
    if data["rssi"] is None:
        return "Missing data", 400

    if not isinstance(data["rssi"], (int)):
        return "Invalid rssi", 400

    CONFIG_VALUES["rssi_threshold"] = data["rssi"]
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
        # Light intensity handled by MQTT

        socketio.emit(
            "dht_update",
            {
                "temperature": SENSOR_VALUES["temperature"],
                "humidity": SENSOR_VALUES["humidity"],
            },
        )

        time.sleep(1)


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

        # No login, so don't go through
        if not user_info:
            time.sleep(1)
            continue

        # Handle light intensity
        # if SENSOR_VALUES["light_intensity"] is not None:
        light = SENSOR_VALUES["light_intensity"]
        prefered_light = user_info["favourites"]["light_intensity"]

        if not (light is None):
            if (
                light < prefered_light
                and email_cooldown["light_intensity"] <= cur_time
                and not STATES["light"]
            ):
                # Change the light
                set_light(True)

                # Send the email
                email_cooldown["light_intensity"] = cur_time + EMAIL_TIMEOUT
                email_client.send_light_email(NOTIFICATION_EMAIL)

                print("[Main] Sent light email!")

        if (light > prefered_light and STATES["light"]):
            # Change the light
            set_light(False)

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


# This thread handles the MQTT connection
def mqtt_thread():
    LIGHT_TOPIC = "room/light_intensity"
    RFID_TOPIC = "room/rfid_reader"

    def on_light(value):
        # Update light intensity
        SENSOR_VALUES["light_intensity"] = value
        socketio.emit("light_intensity_update", SENSOR_VALUES["light_intensity"])

    def on_rfid(value):
        # Get user ID from tag, make sure it's an existing tag
        new_user_id = get_user_id_from_tag(value)
        if not new_user_id:
            return

        # Make sure the user is currently logged out
        if user_info:
            print("[Main] Cannot login: must log out first")
            return

        # Update the user
        update_user(new_user_id)
        email_client.send_login_email(user_info, NOTIFICATION_EMAIL)

    # Make the client, initiate callbacks
    client = MQTTClient(
        host="localhost", port=1883, topics=[(LIGHT_TOPIC, 0), (RFID_TOPIC, 0)]
    )
    client.set_callback(topic=LIGHT_TOPIC, callback=on_light, datatype=int)
    client.set_callback(topic=RFID_TOPIC, callback=on_rfid, datatype=str)

    client.connect()


def bluetooth_thread():
    while True:
        # TODO: check with the rssi threshold
        # Get nearby bluetooth devices
        with open("bl.out") as file:
            bl_count = 0

            for line in file:
                columns = line.split()
                if len(columns) <= 1:
                    continue

                if int(columns[1]) > CONFIG_VALUES["rssi_threshold"]:
                    bl_count += 1
            
            SENSOR_VALUES["devices"] = bl_count

        socketio.emit("devices_update", SENSOR_VALUES["devices"])
        time.sleep(1)


if __name__ == "__main__":
    try:
        Thread(target=bluetooth_thread).start()
        Thread(target=sensor_thread).start()
        Thread(target=email_thread).start()
        Thread(target=mqtt_thread).start()
        app.run(host="0.0.0.0", port=3333)
    except KeyboardInterrupt:
        print("Interrupted by keyboard")
    except Exception as e:
        print("Other error or exception occurred!", e)
    finally:
        GPIO.cleanup()  # Ensures a clean exit
