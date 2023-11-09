# Dependencies
import os
import random
import shutil
import sqlite3
import string
from tkinter import filedialog

# Utilities
from app.utils.database import get_user_id_from_tag, DATABASE_NAME
from app.utils.mqtt import MQTTClient


def generate_random_string(length):
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet) for i in range(length))


RFID_TOPIC = "room/rfid_reader"
print("[User Create] Enter the following information:")

name = input("- Name: ")
description = input("- Description: ")

# Avatar prompt
print("[User Create] Select a profile picture...")

file_types = "*.png *.jpg *.jpeg *.bmp"
avatar_path = filedialog.askopenfilename(filetypes=[("Image files", file_types)])

if avatar_path:
    _, extension = os.path.splitext(os.path.basename(avatar_path))
    random_name = generate_random_string(16) + extension

    new_path = os.path.join("./static/images/", random_name)

    shutil.copy(avatar_path, new_path)
    avatar_path = f"/static/images/{random_name}"
else:
    avatar_path = "/static/images/default-user.jpg"

print(avatar_path) 
print("[User Create] Scan your RFID tag...")


def on_rfid(rfid_tag):
    if not name or not description or not avatar_path:
        return

    if get_user_id_from_tag(rfid_tag) is not None:
        print("[User Create] User already exists!")
        exit(1)

    # Make the new user
    print("[User Create] Creating user...")
    with sqlite3.connect(DATABASE_NAME) as con:
        cur = con.cursor()
        cur.execute(
            """INSERT OR IGNORE INTO users (
            rfid_tag,
            name,
            description,
            avatar,
            temp_threshold,
            humidity_threshold,
            light_threshold
        )
        VALUES (?, ?, ?, ?, 24, 50, 400)""",
            (rfid_tag, name, description, avatar_path),
        )

        con.commit()
        print(f"[User Create] Created user! ID: {cur.lastrowid}, Tag: {rfid_tag}")
        exit(0)


client = MQTTClient(host="localhost", port=1883, topics=[(RFID_TOPIC, 0)])
client.set_callback(topic=RFID_TOPIC, callback=on_rfid, datatype=str)
client.connect()
